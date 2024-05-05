#include <VKL/VKL.h>

VKLFramebuffer::VKLFramebuffer() : VKLCreator<VKLFramebufferCreateInfo>("VKLFramebuffer") {
	
}

VKLFramebuffer::VKLFramebuffer(const VKLFramebufferCreateInfo& createInfo) : VKLCreator<VKLFramebufferCreateInfo>("VKLFramebuffer") {
	create(createInfo);
}

VkExtent2D VKLFramebuffer::size() const {
	return m_size;
}

const VKLRenderPass* VKLFramebuffer::renderPass() const {
	return m_renderPass;
}

const VkClearValue* VKLFramebuffer::clearValues() const {
	return m_clearValues;
}

const std::vector<const VKLImageView*>& VKLFramebuffer::attachments() const {
	return m_attachments;
}

void VKLFramebuffer::setClearValue(VkClearValue clearValue, uint32_t index) {
	m_clearValues[index] = clearValue;
}

void VKLFramebuffer::_create(const VKLFramebufferCreateInfo& createInfo) {
	m_renderPass = createInfo.m_renderPass;
	m_device = m_renderPass->device();
	m_attachments = createInfo.m_attachments;
	m_size.width = createInfo.m_createInfo.width;
	m_size.height =createInfo.m_createInfo.height;
	
	m_clearValues = (VkClearValue*)malloc(sizeof(VkClearValue) * m_attachments.size());
	
	for(int i = 0; i < m_attachments.size(); i++) {
		m_clearValues[i].color.float32[0] = 1.0f;
		m_clearValues[i].color.float32[1] = 0.0f;
		m_clearValues[i].color.float32[2] = 1.0f;
		m_clearValues[i].color.float32[3] = 1.0f;
	}
	
	VK_CALL(m_device->vk.CreateFramebuffer(m_device->handle(), &createInfo.m_createInfo, m_device->allocationCallbacks(), &m_handle));
}

void VKLFramebuffer::_destroy() {
	m_device->vk.DestroyFramebuffer(m_device->handle(), m_handle, m_device->allocationCallbacks());
	
	free(m_clearValues);
}

VKLFramebufferCreateInfo::VKLFramebufferCreateInfo() {
	memset(&m_createInfo, 0, sizeof(VkFramebufferCreateInfo));
	m_createInfo.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
	m_createInfo.pNext = NULL;
	m_createInfo.flags = 0;
	m_createInfo.attachmentCount = 0;
	m_createInfo.pAttachments = NULL;
	m_createInfo.renderPass = (VkRenderPass)VK_NULL_HANDLE;
	m_createInfo.width = 0;
	m_createInfo.height = 0;
	m_createInfo.layers = 0;
	
	m_renderPass = NULL;
}

VKLFramebufferCreateInfo& VKLFramebufferCreateInfo::renderPass(const VKLRenderPass* renderPass) {
	m_renderPass = renderPass;
	m_createInfo.renderPass = m_renderPass->handle();
	
	return invalidate();
}

VKLFramebufferCreateInfo& VKLFramebufferCreateInfo::addAttachment(const VKLImageView* imageView) {
	m_attachments.push_back(imageView);
	m_attachmentsBuffer.push_back(imageView->handle());
	
	return invalidate();
}

VKLFramebufferCreateInfo& VKLFramebufferCreateInfo::extent(uint32_t width, uint32_t height, uint32_t layers) {
	m_createInfo.width = width;
	m_createInfo.height = height;
	m_createInfo.layers = layers;
	
	return invalidate();
}

bool VKLFramebufferCreateInfo::_validate() {
	if (m_renderPass == NULL) {
		printf("VKL Validation Error: VKLFramebufferCreateInfo::renderPass was not set!\n");
		return false;
	}
	
	if(m_renderPass->m_attachmentCount != m_attachments.size()) {
		printf("VKL Validation Error: VKLFramebufferCreateInfo::attachmentCount (%lu) != VKLRenderPass::attachmentCount (%u)!\n", m_attachments.size(), m_renderPass->m_attachmentCount);
		return false;
	}
	
	m_createInfo.attachmentCount = m_attachmentsBuffer.size();
	m_createInfo.pAttachments = m_attachmentsBuffer.data();
	
	return true;
}
