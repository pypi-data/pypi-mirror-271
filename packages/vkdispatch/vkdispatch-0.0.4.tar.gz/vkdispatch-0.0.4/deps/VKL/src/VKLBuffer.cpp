#include <VKL/VKL.h>

VKLBuffer::VKLBuffer() : VKLCreator<VKLBufferCreateInfo>("VKLBuffer") {
	m_device = NULL;
	
	memset(&m_memoryBarrier, 0, sizeof(VkBufferMemoryBarrier));
	m_memoryBarrier.sType = VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER;
	m_memoryBarrier.pNext = NULL;
	m_memoryBarrier.srcAccessMask = 0;
	m_memoryBarrier.dstAccessMask = 0;
	m_memoryBarrier.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
	m_memoryBarrier.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
	m_memoryBarrier.offset = 0;
}


VKLBuffer::VKLBuffer(const VKLBufferCreateInfo& createInfo) : VKLCreator<VKLBufferCreateInfo>("VKLBuffer")  {
	memset(&m_memoryBarrier, 0, sizeof(VkBufferMemoryBarrier));
	m_memoryBarrier.sType = VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER;
	m_memoryBarrier.pNext = NULL;
	m_memoryBarrier.srcAccessMask = 0;
	m_memoryBarrier.dstAccessMask = 0;
	m_memoryBarrier.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
	m_memoryBarrier.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
	m_memoryBarrier.offset = 0;
	
	this->create(createInfo);
}

void* VKLBuffer::map() {
	void* result;
	
	if (m_allocation.vma_enabled)
		VK_CALL(vmaMapMemory(m_device->allocatorVMA(), m_allocation.vma_allocation, &result)) 
	else
		VK_CALL(m_device->vk.MapMemory(m_device->handle(), m_allocation.memory, m_allocation.offset, m_allocation.size, 0, &result));

	return result;
}
void VKLBuffer::unmap() {
	if (m_allocation.vma_enabled)
		vmaUnmapMemory(m_device->allocatorVMA(), m_allocation.vma_allocation);
	else
		m_device->vk.UnmapMemory(m_device->handle(), m_allocation.memory);
}

void VKLBuffer::setData(void* data, size_t size, size_t offset) {
	uint8_t* mappedData = (uint8_t*)map();
	memcpy(mappedData + offset, data, size);
	unmap();
}

void VKLBuffer::getData(void* data, size_t size, size_t offset) {
	uint8_t* mappedData = (uint8_t*)map();
	memcpy(data, mappedData + offset, size);
	unmap();
}

VKLAllocation VKLBuffer::allocation() const {
	return m_allocation;
}

VkMemoryRequirements VKLBuffer::memoryRequirements() const {
	VkMemoryRequirements memoryRequirements;
	m_device->vk.GetBufferMemoryRequirements(m_device->handle(), m_handle, &memoryRequirements);
	return memoryRequirements;
}

void VKLBuffer::setNewAccessMask(VkAccessFlags accessMask) {
	m_memoryBarrier.dstAccessMask = accessMask;
}

VkBufferMemoryBarrier* VKLBuffer::getMemoryBarrier() {
	return &m_memoryBarrier;
}


void VKLBuffer::resetBarrier() {
	m_memoryBarrier.srcAccessMask = m_memoryBarrier.dstAccessMask;
}

void VKLBuffer::copyFrom(VKLBuffer* src, const VKLQueue* transferQueue, VkBufferCopy bufferCopy) {
	transferQueue->getCmdBuffer()->begin();
	transferQueue->getCmdBuffer()->copyBuffer(this, src, bufferCopy);
	transferQueue->getCmdBuffer()->end();
	
	transferQueue->submitAndWait(transferQueue->getCmdBuffer());
}

void VKLBuffer::uploadData(const VKLQueue* transferQueue, void* data, size_t size, size_t offset) {
	VKLBuffer tempStageBuffer(
		VKLBufferCreateInfo()
		.device(m_device)
		.size(size)
		.usageVMA(VMA_MEMORY_USAGE_AUTO_PREFER_HOST)
		.flagsVMA(VMA_ALLOCATION_CREATE_HOST_ACCESS_SEQUENTIAL_WRITE_BIT)
		.usage(VK_BUFFER_USAGE_TRANSFER_SRC_BIT)
	);

	tempStageBuffer.setData(data, size, 0);
	
	VkBufferCopy bufferCopy;
	bufferCopy.size = size;
	bufferCopy.dstOffset = offset;
	bufferCopy.srcOffset = 0;

	this->copyFrom(&tempStageBuffer, transferQueue, bufferCopy);
	
	tempStageBuffer.destroy();
}

void VKLBuffer::downloadData(const VKLQueue* transferQueue, void* data, size_t size, size_t offset) {
	VKLBuffer tempStageBuffer(
		VKLBufferCreateInfo()
		.device(m_device)
		.size(size)
		.usageVMA(VMA_MEMORY_USAGE_AUTO_PREFER_HOST)
		.flagsVMA(VMA_ALLOCATION_CREATE_HOST_ACCESS_RANDOM_BIT)
		.usage(VK_BUFFER_USAGE_TRANSFER_DST_BIT)
	);

	VkBufferCopy bufferCopy;
	bufferCopy.size = size;
	bufferCopy.dstOffset = 0;
	bufferCopy.srcOffset = offset;
	
	tempStageBuffer.copyFrom(this, transferQueue, bufferCopy);	
	tempStageBuffer.getData(data, size, 0);
	
	tempStageBuffer.destroy();
}

void VKLBuffer::_create(const VKLBufferCreateInfo& createInfo) {
	m_device = createInfo.m_device;

	if(createInfo.useVMAFlag) {
		VmaAllocationCreateInfo vmaAllocationCreateInfo = {};
		vmaAllocationCreateInfo.flags = createInfo.flagsVMAFlag;
		vmaAllocationCreateInfo.usage = createInfo.usageVMAFlag;
		vmaAllocationCreateInfo.pUserData = &m_allocation;

		VK_CALL(vmaCreateBuffer(m_device->allocatorVMA() , &createInfo.m_bufferCreateInfo, &vmaAllocationCreateInfo, &m_handle, &m_allocation.vma_allocation, &m_allocation.vma_allocation_info));

		m_allocation.vma_enabled = 1;
	} else {
		VK_CALL(m_device->vk.CreateBuffer(m_device->handle(), &createInfo.m_bufferCreateInfo, m_device->allocationCallbacks(), &m_handle));
		m_allocation.vma_enabled = 0;
	}

	m_memoryBarrier.buffer = m_handle;
	m_memoryBarrier.size = createInfo.m_bufferCreateInfo.size;

	m_allocation.buffer = this;
}

void VKLBuffer::bind(VKLAllocation allocation) {
	if(m_allocation.vma_enabled) {
		LOG_ERROR("Cannot bind memory for VMA buffer");
		return;
	}

	LOG_INFO("Binding buffer to memory: %d, %d, %d", allocation.memory, allocation.offset, allocation.size);

	m_allocation.memory = allocation.memory;
	m_allocation.offset = allocation.offset;
	m_allocation.size = allocation.size;

	VK_CALL(m_device->vk.BindBufferMemory(m_device->handle(), m_handle, m_allocation.memory, m_allocation.offset));
}

void VKLBuffer::_destroy() {
	if(m_allocation.vma_enabled)
		vmaDestroyBuffer(m_device->allocatorVMA(), m_handle, m_allocation.vma_allocation);
	else
		m_device->vk.DestroyBuffer(m_device->handle(), m_handle, m_device->allocationCallbacks());
}

VKLBufferCreateInfo::VKLBufferCreateInfo() {
	m_device = NULL;
	
	memset(&m_bufferCreateInfo, 0, sizeof(VkBufferCreateInfo));
	m_bufferCreateInfo.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
	m_bufferCreateInfo.pNext = NULL;
	m_bufferCreateInfo.flags = 0;
	m_bufferCreateInfo.usage = 0;
	m_bufferCreateInfo.size = 0;
	m_bufferCreateInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
	m_bufferCreateInfo.queueFamilyIndexCount = 0;
	m_bufferCreateInfo.pQueueFamilyIndices = NULL;

	useVMAFlag = true;
	usageVMAFlag = VMA_MEMORY_USAGE_AUTO_PREFER_DEVICE;
	flagsVMAFlag = 0;
}

VKLBufferCreateInfo& VKLBufferCreateInfo::pNext(void* pNext) {
	m_bufferCreateInfo.pNext = pNext;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::device(const VKLDevice* device) {
	m_device = device;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::size(VkDeviceSize size) {
	m_bufferCreateInfo.size = size;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::usage(VkBufferUsageFlags usage) {
	m_bufferCreateInfo.usage = usage;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::useVMA(bool useVMA) {
	useVMAFlag = useVMA;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::usageVMA(VmaMemoryUsage usage) {
	usageVMAFlag = usage;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::flagsVMA(VmaAllocationCreateFlags flags) {
	flagsVMAFlag = flags;
	
	return invalidate();
}

VKLBufferCreateInfo& VKLBufferCreateInfo::memoryProperties(VkMemoryPropertyFlags memoryProperties) {
	m_bufferCreateInfo.usage = memoryProperties;
	
	return invalidate();
}

bool VKLBufferCreateInfo::_validate() {
	if(m_device == NULL) {
		printf("VKL Validation Error: VKLBufferCreateInfo::device is not set!\n");
		return false;
	}

	if (m_bufferCreateInfo.size == 0) {
		printf("VKL Validation Error: VKLBufferCreateInfo::size is not set!\n");
		return false;
	}
	
	return true;
}
