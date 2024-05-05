#include <VKL/VKL.h>

VKLDescriptorSet::VKLDescriptorSet(const VKLPipelineLayout* layout, uint32_t set) {
	m_layout = layout;
	m_device = m_layout->device();
	m_set = set;
	
	VkDescriptorPoolCreateInfo descriptorPoolCreateInfo;
	memset(&descriptorPoolCreateInfo, 0, sizeof(VkDescriptorPoolCreateInfo));
	descriptorPoolCreateInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
	descriptorPoolCreateInfo.maxSets = 1;
	descriptorPoolCreateInfo.poolSizeCount = m_layout->m_descriptorPoolSizes[set].size();
	descriptorPoolCreateInfo.pPoolSizes = m_layout->m_descriptorPoolSizes[set].data();

	VK_CALL(m_device->vk.CreateDescriptorPool(m_device->handle(), &descriptorPoolCreateInfo, NULL, &m_pool));

	VkDescriptorSetAllocateInfo descriptorSetAllocateInfo;
	memset(&descriptorSetAllocateInfo, 0, sizeof(VkDescriptorSetAllocateInfo));
	descriptorSetAllocateInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
	descriptorSetAllocateInfo.descriptorPool = m_pool;
	descriptorSetAllocateInfo.descriptorSetCount = 1;
	descriptorSetAllocateInfo.pSetLayouts = &m_layout->descriptorSetLayouts()[set];

	VK_CALL(m_device->vk.AllocateDescriptorSets(m_device->handle(), &descriptorSetAllocateInfo, &m_handle));
}

VkDescriptorPool VKLDescriptorSet::pool() const {
	return m_pool;
}

const VKLPipelineLayout* VKLDescriptorSet::layout() const {
	return m_layout;
}

const VKLDevice* VKLDescriptorSet::device() const {
	return m_layout->device();
}

uint32_t VKLDescriptorSet::set() const {
	return m_set;
}

//void VKLDescriptorSet::bind(const VKLCommandBuffer* cmdBuffer) const {
//	m_device->vk.CmdBindDescriptorSets(cmdBuffer->handle(), VK_PIPELINE_BIND_POINT_GRAPHICS, m_shader->pipelineLayout(), m_set, 1, &m_handle, 0, NULL);
//}

void VKLDescriptorSet::writeImage(uint32_t binding, VkDescriptorType type, VkImageView view, VkImageLayout layout, VkSampler sampler) {
	VkDescriptorImageInfo descriptorImageInfo;
	memset(&descriptorImageInfo, 0, sizeof(VkDescriptorImageInfo));
	descriptorImageInfo.sampler = sampler;
	descriptorImageInfo.imageView = view;
	descriptorImageInfo.imageLayout = layout;

	VkWriteDescriptorSet writeDescriptor;
	memset(&writeDescriptor, 0, sizeof(VkWriteDescriptorSet));
	writeDescriptor.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
	writeDescriptor.dstSet = m_handle;
	writeDescriptor.dstBinding = binding;
	writeDescriptor.dstArrayElement = 0;
	writeDescriptor.descriptorCount = 1;
	writeDescriptor.descriptorType = type;
	writeDescriptor.pImageInfo = &descriptorImageInfo;
	writeDescriptor.pBufferInfo = NULL;
	writeDescriptor.pTexelBufferView = NULL;

	m_device->vk.UpdateDescriptorSets(m_device->handle(), 1, &writeDescriptor, 0, NULL);
}

void VKLDescriptorSet::writeBuffer(uint32_t binding, VkDescriptorType type, const VKLBuffer* buffer, VkDeviceSize offset, VkDeviceSize range) {
	VkDescriptorBufferInfo buffDesc;
	buffDesc.buffer = buffer->handle();
	buffDesc.offset = offset;
	buffDesc.range = range;

	VkWriteDescriptorSet writeDescriptor;
	memset(&writeDescriptor, 0, sizeof(VkWriteDescriptorSet));
	writeDescriptor.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
	writeDescriptor.dstSet = m_handle;
	writeDescriptor.dstBinding = binding;
	writeDescriptor.dstArrayElement = 0;
	writeDescriptor.descriptorCount = 1;
	writeDescriptor.descriptorType = type;
	writeDescriptor.pImageInfo = NULL;
	writeDescriptor.pBufferInfo = &buffDesc;
	writeDescriptor.pTexelBufferView = NULL;

	m_device->vk.UpdateDescriptorSets(m_device->handle(), 1, &writeDescriptor, 0, NULL);
}

void VKLDescriptorSet::destroy() {
	m_device->vk.DestroyDescriptorPool(m_device->handle(), m_pool, m_device->allocationCallbacks());
}
