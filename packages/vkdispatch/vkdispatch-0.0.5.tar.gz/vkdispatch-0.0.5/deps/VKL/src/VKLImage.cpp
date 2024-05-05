#include <VKL/VKL.h>

VKLImage::VKLImage() : VKLCreator<VKLImageCreateInfo>("VKLImage") {
	m_device = NULL;
	m_handle = (VkImage)VK_NULL_HANDLE;
	m_aspect = VK_IMAGE_ASPECT_COLOR_BIT;
}

VKLImage::VKLImage(const VKLImageCreateInfo& createInfo) : VKLCreator<VKLImageCreateInfo>("VKLImage") {
	m_device = NULL;
	m_handle = (VkImage)VK_NULL_HANDLE;
	m_aspect = VK_IMAGE_ASPECT_COLOR_BIT;
	create(createInfo);
}

void VKLImage::_create(const VKLImageCreateInfo& createInfo) {
	_create(createInfo, (VkImage)VK_NULL_HANDLE);
}

void VKLImage::_create(const VKLImageCreateInfo& createInfo, VkImage handle) {
	m_device = createInfo.m_device;
	m_format = createInfo.m_imageCreateInfo.format;
	m_size = createInfo.m_imageCreateInfo.extent;
	m_layers = createInfo.m_imageCreateInfo.arrayLayers;
	
	if(handle == VK_NULL_HANDLE) {
		if(createInfo.useVMAFlag) {
			VmaAllocationCreateInfo vmaAllocationCreateInfo = {};
			vmaAllocationCreateInfo.flags = createInfo.flagsVMAFlag;
			vmaAllocationCreateInfo.usage = createInfo.usageVMAFlag;
			vmaAllocationCreateInfo.pUserData = &m_allocation;
			
			VK_CALL(vmaCreateImage(m_device->allocatorVMA(), &createInfo.m_imageCreateInfo, &vmaAllocationCreateInfo, &m_handle, &m_allocation.vma_allocation, &m_allocation.vma_allocation_info));
			
			m_allocation.vma_enabled = 1;
		} else {
			VK_CALL(m_device->vk.CreateImage(m_device->handle(), &createInfo.m_imageCreateInfo, m_device->allocationCallbacks(), &m_handle));

			m_allocation.vma_enabled = 0;
		}		

		m_memoryBarrier.oldLayout = createInfo.m_imageCreateInfo.initialLayout;
	} else {
		m_handle = handle;

		initBarrier(createInfo.m_imageCreateInfo.initialLayout);
	}
}

void VKLImage::bind(VKLAllocation allocation) {
	if(m_allocation.vma_enabled) {
		LOG_ERROR("Cannot bind memory for VMA image");
		return;
	}

		LOG_INFO("Binding image to memory: %d, %d, %d", allocation.memory, allocation.offset, allocation.size);

	m_allocation.memory = allocation.memory;
	m_allocation.offset = allocation.offset;
	m_allocation.size = allocation.size;
	
	VK_CALL(m_device->vk.BindImageMemory(m_device->handle(), m_handle, m_allocation.memory, m_allocation.offset));	
	
	initBarrier(m_memoryBarrier.oldLayout);
}

void VKLImage::initBarrier(VkImageLayout layout) {
	m_memoryBarrier.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
	m_memoryBarrier.pNext = NULL;
	m_memoryBarrier.srcAccessMask = 0;
	m_memoryBarrier.dstAccessMask = 0;
	m_memoryBarrier.oldLayout = layout;
	m_memoryBarrier.newLayout = layout;
	m_memoryBarrier.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
	m_memoryBarrier.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
	m_memoryBarrier.image = m_handle;
	m_memoryBarrier.subresourceRange.aspectMask = m_aspect;
	m_memoryBarrier.subresourceRange.baseMipLevel = 0;
	m_memoryBarrier.subresourceRange.levelCount = 1;
	m_memoryBarrier.subresourceRange.baseArrayLayer = 0;
	m_memoryBarrier.subresourceRange.layerCount = m_layers;
}

VkAccessFlags VKLImage::accessMask() const {
	return m_memoryBarrier.dstAccessMask;
}

VkImageLayout VKLImage::layout() const {
	return m_memoryBarrier.newLayout;
}

VkImageAspectFlags VKLImage::aspect() const {
	return m_aspect;
}

VkExtent3D VKLImage::extent() const {
	return m_size;
}

int VKLImage::layers() const {
	return m_layers;
}

VKLAllocation VKLImage::allocation() const {
	return m_allocation;
}

VkMemoryRequirements VKLImage::memoryRequirements() const {
	VkMemoryRequirements memoryRequirements;
	m_device->vk.GetImageMemoryRequirements(m_device->handle(), m_handle, &memoryRequirements);

	return memoryRequirements;
}

void VKLImage::cmdTransitionBarrier(VKLCommandBuffer* cmdBuffer, VkAccessFlags accessMask, VkImageLayout layout, VkPipelineStageFlags srcStageMask, VkPipelineStageFlags dstStageMask) {
	m_memoryBarrier.dstAccessMask = accessMask;
	m_memoryBarrier.newLayout = layout;
	
	m_device->vk.CmdPipelineBarrier(cmdBuffer->handle(), srcStageMask, dstStageMask, 0, 0, NULL, 0, NULL, 1, &m_memoryBarrier);
	
	m_memoryBarrier.srcAccessMask = m_memoryBarrier.dstAccessMask;
	m_memoryBarrier.oldLayout = m_memoryBarrier.newLayout;
}

void VKLImage::transition(const VKLQueue* queue, VkAccessFlags accessMask, VkImageLayout layout, VkPipelineStageFlags srcStageMask, VkPipelineStageFlags dstStageMask) {
	queue->getCmdBuffer()->begin();
	cmdTransitionBarrier(queue->getCmdBuffer(), accessMask, layout, srcStageMask, dstStageMask);
	queue->getCmdBuffer()->end();
	queue->submitAndWait(queue->getCmdBuffer());
}

VkFormat VKLImage::format() const {
	return m_format;
}

void VKLImage::copyFrom(VKLImage* src, const VKLQueue* transferQueue, VkImageCopy imageCopy) {
	transferQueue->getCmdBuffer()->begin();
	transferQueue->getCmdBuffer()->copyImage(this, src, imageCopy);
	transferQueue->getCmdBuffer()->end();
	transferQueue->submitAndWait(transferQueue->getCmdBuffer());
}

void VKLImage::setData(void* data, size_t size, size_t pixelSize) {
	VkImageSubresource subresource;
	memset(&subresource, 0, sizeof(VkImageSubresource));
	subresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
	subresource.mipLevel = 0;
	subresource.arrayLayer = 0;

	VkSubresourceLayout imageLayout;
	m_device->vk.GetImageSubresourceLayout(m_device->handle(), m_handle, &subresource, &imageLayout);

	uint32_t textureRowWidth = m_size.width * pixelSize;
	
	uint8_t* mappedData;
	VK_CALL(m_device->vk.MapMemory(m_device->handle(), m_allocation.memory, m_allocation.offset, m_allocation.size, 0, (void**)&mappedData));

	if (imageLayout.rowPitch == textureRowWidth) {
		memcpy(mappedData, data, m_size.height * textureRowWidth);
	}
	else {
		uint8_t* mappedBytes = (uint8_t*)mappedData;
		uint8_t* dataBytes = (uint8_t*)data;

		for (int y = 0; y < m_size.height; y++) {
			memcpy(&mappedBytes[y * imageLayout.rowPitch],
					&dataBytes[y * textureRowWidth],
					textureRowWidth);
		}
	}

	m_device->vk.UnmapMemory(m_device->handle(), m_allocation.memory);
}

void VKLImage::getData(void* data, size_t size, size_t pixelSize) {
	VkImageSubresource subresource;
	memset(&subresource, 0, sizeof(VkImageSubresource));
	subresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
	subresource.mipLevel = 0;
	subresource.arrayLayer = 0;

	VkSubresourceLayout imageLayout;
	m_device->vk.GetImageSubresourceLayout(m_device->handle(), m_handle, &subresource, &imageLayout);

	uint32_t textureRowWidth = m_size.width * pixelSize;

	uint8_t* mappedData;

	VK_CALL(m_device->vk.MapMemory(m_device->handle(), m_allocation.memory, m_allocation.offset, m_allocation.size, 0, (void**)&mappedData));
	if (imageLayout.rowPitch == textureRowWidth) {
		memcpy(data, mappedData, m_size.height * textureRowWidth);
	}
	else {
		uint8_t* mappedBytes = (uint8_t*)mappedData;
		uint8_t* dataBytes = (uint8_t*)data;

		for (int y = 0; y < m_size.height; y++) {
			memcpy(&dataBytes[y * textureRowWidth],
					&mappedBytes[y * imageLayout.rowPitch],
					textureRowWidth);
		}
	}

	m_device->vk.UnmapMemory(m_device->handle(), m_allocation.memory);
}

void VKLImage::uploadData(const VKLQueue* transferQueue, void* data, size_t size, size_t pixelSize) {
	VKLImage stagingImage(VKLImageCreateInfo()
							.device(m_device)
							.extent(m_size.width, m_size.height, m_size.depth)
							.format(m_format)
							.tiling(VK_IMAGE_TILING_LINEAR)
							.usage(VK_IMAGE_USAGE_TRANSFER_SRC_BIT)
							.initialLayout(VK_IMAGE_LAYOUT_PREINITIALIZED)
							.memoryProperties(VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)
							.arrayLayers(m_layers));
	
	VKLAllocation allocation;
	allocation.memory = m_device->allocateMemory(stagingImage.memoryRequirements(), 
													VK_MEMORY_PROPERTY_HOST_COHERENT_BIT | VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT);
	allocation.offset = 0;
	allocation.size = stagingImage.memoryRequirements().size;

	stagingImage.bind(allocation);
	
	stagingImage.setData(data, size, pixelSize);
	
	VkImageCopy imageCopy;
	memset(&imageCopy, 0, sizeof(VkImageCopy));
	imageCopy.srcSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
	imageCopy.srcSubresource.layerCount = m_layers;
	imageCopy.dstSubresource = imageCopy.srcSubresource;
	imageCopy.extent = m_size;
	
	transferQueue->getCmdBuffer()->begin();
	
	stagingImage.cmdTransitionBarrier(transferQueue->getCmdBuffer(),
									  VK_ACCESS_TRANSFER_READ_BIT, VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
									  VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT);
	
	transferQueue->getCmdBuffer()->copyImage(this, &stagingImage, imageCopy);
	transferQueue->getCmdBuffer()->end();
	
	transferQueue->submitAndWait(transferQueue->getCmdBuffer());
	
	stagingImage.destroy();

	m_device->vk.FreeMemory(m_device->handle(), allocation.memory, m_device->allocationCallbacks());
}


void VKLImage::uploadDataBuffer(const VKLQueue* transferQueue, void* data, size_t size) {
	VKLBuffer stagingBuffer(VKLBufferCreateInfo()
							.device(m_device)
							.size(size)
							.usage(VK_BUFFER_USAGE_TRANSFER_SRC_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT)
							.memoryProperties(VK_MEMORY_PROPERTY_HOST_COHERENT_BIT | VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT));
	
	VKLAllocation allocation;
	allocation.memory = m_device->allocateMemory(stagingBuffer.memoryRequirements(), 
													VK_MEMORY_PROPERTY_HOST_COHERENT_BIT | VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT);
	allocation.offset = 0;
	allocation.size = stagingBuffer.memoryRequirements().size;	
	
	stagingBuffer.bind(allocation);
	
	stagingBuffer.setData(data, size, 0);

	VkBufferImageCopy bufferImageCopy;
	memset(&bufferImageCopy, 0, sizeof(VkBufferImageCopy));
	bufferImageCopy.bufferOffset = 0;
	bufferImageCopy.bufferRowLength = 0;
	bufferImageCopy.bufferImageHeight = 0;
	bufferImageCopy.imageSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
	bufferImageCopy.imageSubresource.layerCount = m_layers;
	bufferImageCopy.imageExtent = m_size;
	
	transferQueue->getCmdBuffer()->begin();
	
	this->cmdTransitionBarrier(transferQueue->getCmdBuffer(),
							   VK_ACCESS_TRANSFER_WRITE_BIT, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
							   VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT);

	m_device->vk.CmdCopyBufferToImage(
		transferQueue->getCmdBuffer()->handle(),
		stagingBuffer.handle(),
		this->handle(),
		VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
		1,
		&bufferImageCopy
	);

	transferQueue->getCmdBuffer()->end();
	
	transferQueue->submitAndWait(transferQueue->getCmdBuffer());
	
	stagingBuffer.destroy();
	m_device->vk.FreeMemory(m_device->handle(), allocation.memory, m_device->allocationCallbacks());
}


void VKLImage::downloadDataBuffer(const VKLQueue* transferQueue, void* data, size_t size) {
	VKLBuffer stagingBuffer(VKLBufferCreateInfo()
							.device(m_device)
							.size(size)
							.usage(VK_BUFFER_USAGE_TRANSFER_SRC_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT)
							.memoryProperties(VK_MEMORY_PROPERTY_HOST_COHERENT_BIT | VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT));
	
	VKLAllocation allocation;
	allocation.memory = m_device->allocateMemory(stagingBuffer.memoryRequirements(), 
													VK_MEMORY_PROPERTY_HOST_COHERENT_BIT | VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT);
	allocation.offset = 0;
	allocation.size = stagingBuffer.memoryRequirements().size;

	stagingBuffer.bind(allocation);

	VkBufferImageCopy bufferImageCopy;
	memset(&bufferImageCopy, 0, sizeof(VkBufferImageCopy));
	bufferImageCopy.bufferOffset = 0;
	bufferImageCopy.bufferRowLength = 0;
	bufferImageCopy.bufferImageHeight = 0;
	bufferImageCopy.imageSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
	bufferImageCopy.imageSubresource.layerCount = m_layers;
	bufferImageCopy.imageExtent = m_size;
	
	transferQueue->getCmdBuffer()->begin();
	
	this->cmdTransitionBarrier(transferQueue->getCmdBuffer(),
							   VK_ACCESS_TRANSFER_READ_BIT, VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
							   VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT);

	m_device->vk.CmdCopyImageToBuffer(
		transferQueue->getCmdBuffer()->handle(),
		this->handle(), 
		VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
		stagingBuffer.handle(),
		1,
		&bufferImageCopy
	);

	transferQueue->getCmdBuffer()->end();
	
	transferQueue->submitAndWait(transferQueue->getCmdBuffer());
	
	stagingBuffer.getData(data, size, 0);
	
	stagingBuffer.destroy();
	m_device->vk.FreeMemory(m_device->handle(), allocation.memory, m_device->allocationCallbacks());
}

void VKLImage::_destroy() {
	if(m_allocation.vma_enabled)
		vmaDestroyImage(m_device->allocatorVMA(), m_handle, m_allocation.vma_allocation);
	else
		m_device->vk.DestroyImage(m_device->handle(), m_handle, m_device->allocationCallbacks());
}

VKLImageCreateInfo::VKLImageCreateInfo() {
	memset(&m_imageCreateInfo, 0, sizeof(VkImageCreateInfo));
	m_imageCreateInfo.sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO;
	m_imageCreateInfo.pNext = NULL;
	m_imageCreateInfo.flags = 0;
	m_imageCreateInfo.imageType = VK_IMAGE_TYPE_2D;
	m_imageCreateInfo.format = VK_FORMAT_UNDEFINED;
	m_imageCreateInfo.mipLevels = 1;
	m_imageCreateInfo.arrayLayers = 1;
	m_imageCreateInfo.samples = VK_SAMPLE_COUNT_1_BIT;
	m_imageCreateInfo.tiling = VK_IMAGE_TILING_OPTIMAL;
	m_imageCreateInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
	m_imageCreateInfo.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;

	m_memoryProperties = VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT;

	m_allocationPNext = NULL;

	useVMAFlag = true;
	usageVMAFlag = VMA_MEMORY_USAGE_AUTO_PREFER_DEVICE;
	flagsVMAFlag = 0;

	LOG_INFO("Init VKLImageCreateInfo");
}

VKLImageCreateInfo& VKLImageCreateInfo::device(const VKLDevice* device) {
	LOG_INFO("VKLImageCreateInfo::device");

	m_device = device;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::pNext(void* pNext) {
	LOG_INFO("VKLImageCreateInfo::pNext");
	m_imageCreateInfo.pNext = pNext;

	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::allocationPNext(void* pNext) {
	LOG_INFO("VKLImageCreateInfo::allocationPNext");
	m_allocationPNext = pNext;

	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::imageType(VkImageType type) {
	m_imageCreateInfo.imageType = type;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::format(VkFormat format) {
	LOG_INFO("VKLImageCreateInfo::format");
	m_imageCreateInfo.format = format;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::extent(uint32_t width, uint32_t height, uint32_t depth) {
	LOG_INFO("VKLImageCreateInfo::extent");
	m_imageCreateInfo.extent.width = width;
	m_imageCreateInfo.extent.height = height;
	m_imageCreateInfo.extent.depth = depth;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::tiling(VkImageTiling tiling) {
	m_imageCreateInfo.tiling = tiling;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::usage(VkImageUsageFlags usage) {
	LOG_INFO("VKLImageCreateInfo::usage");
	m_imageCreateInfo.usage = usage;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::initialLayout(VkImageLayout layout) {
	m_imageCreateInfo.initialLayout = layout;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::arrayLayers(uint32_t arrayLayers) {
	m_imageCreateInfo.arrayLayers = arrayLayers;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::memoryProperties(VkMemoryPropertyFlags memoryProperties) {
	m_memoryProperties = memoryProperties;

	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::useVMA(bool useVMA) {
	useVMAFlag = useVMA;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::usageVMA(VmaMemoryUsage usage) {
	usageVMAFlag = usage;
	
	return invalidate();
}

VKLImageCreateInfo& VKLImageCreateInfo::flagsVMA(VmaAllocationCreateFlags flags) {
	flagsVMAFlag = flags;
	
	return invalidate();
}

bool VKLImageCreateInfo::_validate() {
	if(m_device == NULL) {
		printf("VKL Validation Error: VKLImageCreateInfo::device is not set!\n");
		return false;
	}
	
	if (m_imageCreateInfo.extent.width == 0 || m_imageCreateInfo.extent.height == 0 || m_imageCreateInfo.extent.depth == 0) {
		printf("VKL Validation Error: VKLImageCreateInfo::extent is zero on at least one dimension!\n");
		return false;
	}

	if (m_imageCreateInfo.format == VK_FORMAT_UNDEFINED) {
		printf("VKL Validation Error: VKLImageCreateInfo::format is not set!\n");
		return false;
	}

	if (m_imageCreateInfo.usage == 0) {
		printf("VKL Validation Error: VKLImageCreateInfo::usage is not set!\n");
		return false;
	}
	
	return true;
}
