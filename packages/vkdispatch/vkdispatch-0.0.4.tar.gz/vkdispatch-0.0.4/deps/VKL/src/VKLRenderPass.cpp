#include <VKL/VKL.h>

VKLRenderPass::VKLRenderPass() : VKLCreator<VKLRenderPassCreateInfo>("VKLRenderPass") {
	m_attachmentCount = 0;
}

VKLRenderPass::VKLRenderPass(const VKLRenderPassCreateInfo& createInfo) : VKLCreator<VKLRenderPassCreateInfo>("VKLRenderPass") {
	m_attachmentCount = 0;
	create(createInfo);
}

const VKLDevice* VKLRenderPass::device() const{
	return m_device;
}

void VKLRenderPass::_destroy() {
	m_device->vk.DestroyRenderPass(m_device->handle(), m_handle, m_device->allocationCallbacks());
}

void VKLRenderPass::_create(const VKLRenderPassCreateInfo& createInfo) {
	m_device = createInfo.m_device;
	m_attachmentCount = createInfo.m_attachmentDescriptions.size();
	
	
	m_subpassCount = createInfo.m_subpassDescriptions.size();
	m_subpassColorAttachmentCounts = (uint32_t*)malloc(sizeof(uint32_t) * m_subpassCount);
	
	for(int i = 0; i < m_subpassCount; i++) {
		m_subpassColorAttachmentCounts[i] = createInfo.m_subpassDescriptions[i].m_colorAttachments.size();
	}
	
	VK_CALL(m_device->vk.CreateRenderPass(m_device->handle(), &createInfo.m_createInfo, m_device->allocationCallbacks(), &m_handle));
}

VKLRenderPassCreateInfo::VKLRenderPassCreateInfo() {
	m_device = NULL;

	memset(&m_createInfo, 0, sizeof(VkRenderPassCreateInfo));
	m_createInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
}

VKLRenderPassCreateInfo& VKLRenderPassCreateInfo::device(const VKLDevice* device) {
	m_device = device;

	return invalidate();
}

VKLAttachmentDescription& VKLRenderPassCreateInfo::addAttachment(VkFormat format) {
	m_attachmentDescriptions.push_back(VKLAttachmentDescription(this, format));

	invalidate();

	return m_attachmentDescriptions.back();
}

VKLSubpassDescription& VKLRenderPassCreateInfo::addSubpass() {
	m_subpassDescriptions.push_back(VKLSubpassDescription(this));

	invalidate();

	return m_subpassDescriptions.back();
}

VKLSubpassDependency& VKLRenderPassCreateInfo::addSubpassDependency(uint32_t srcSubpass, uint32_t dstSubpass, VkDependencyFlags dependencyFlags) {
	m_subpassDependencies.push_back(VKLSubpassDependency(this, srcSubpass, dstSubpass, dependencyFlags));

	invalidate();

	return m_subpassDependencies.back();
}

bool VKLRenderPassCreateInfo::_validate() {
	if (m_device == NULL) {
		printf("VKL Validation Error: VKLRenderPassCreateInfo::device was not set!\n");
		return false;
	}

	m_createInfo.attachmentCount = m_attachmentDescriptionsBuffer.size();
	m_createInfo.pAttachments = m_attachmentDescriptionsBuffer.data();
	m_createInfo.subpassCount = m_subpassDecriptionBuffer.size();
	m_createInfo.pSubpasses = m_subpassDecriptionBuffer.data();
	m_createInfo.dependencyCount = m_subpassDependenciesBuffer.size();
	m_createInfo.pDependencies = m_subpassDependenciesBuffer.data();

	return true;
}

VKLAttachmentDescription& VKLAttachmentDescription::samples(VkSampleCountFlagBits samples) {
	m_desc.samples = samples;

	return *this;
}

VKLAttachmentDescription& VKLAttachmentDescription::op(VkAttachmentLoadOp load, VkAttachmentStoreOp store) {
	m_desc.loadOp = load;
	m_desc.storeOp = store;

	return *this;
}

VKLAttachmentDescription& VKLAttachmentDescription::stencilOp(VkAttachmentLoadOp load, VkAttachmentStoreOp store) {
	m_desc.stencilLoadOp = load;
	m_desc.stencilStoreOp = store;

	return *this;
}

VKLAttachmentDescription& VKLAttachmentDescription::layout(VkImageLayout initialLayout, VkImageLayout finalLayout) {
	m_desc.initialLayout = initialLayout;
	m_desc.finalLayout = finalLayout;

	return *this;
}

VKLRenderPassCreateInfo& VKLAttachmentDescription::end() {
	m_parent->m_attachmentDescriptionsBuffer.push_back(m_desc);

	return *m_parent;
}

VKLAttachmentDescription::VKLAttachmentDescription(VKLRenderPassCreateInfo* parent, VkFormat format) {
	m_desc.flags = 0;
	m_desc.format = format;
	m_desc.samples = VK_SAMPLE_COUNT_1_BIT;
	m_desc.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
	m_desc.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
	m_desc.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
	m_desc.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
	m_desc.initialLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
	m_desc.finalLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;

	m_parent = parent;
}

VKLSubpassDescription& VKLSubpassDescription::addInputAttachment(uint32_t attachment, VkImageLayout layout) {
	VkAttachmentReference result;
	result.attachment = attachment;
	result.layout = layout;

	m_inputAttachments.push_back(result);

	m_desc.pInputAttachments = m_inputAttachments.data();
	m_desc.inputAttachmentCount = m_inputAttachments.size();

	return *this;
}

VKLSubpassDescription& VKLSubpassDescription::addColorAttachment(uint32_t attachment, VkImageLayout layout) {
	VkAttachmentReference result;
	result.attachment = attachment;
	result.layout = layout;

	m_colorAttachments.push_back(result);

	m_desc.pColorAttachments = m_colorAttachments.data();
	m_desc.colorAttachmentCount = m_colorAttachments.size();

	return *this;
}

VKLSubpassDescription& VKLSubpassDescription::depthAttachment(uint32_t attachment, VkImageLayout layout) {
	VkAttachmentReference* depthAttachment = (VkAttachmentReference*)malloc(sizeof(VkAttachmentReference));
	depthAttachment->layout = layout;
	depthAttachment->attachment = attachment;
	
	m_desc.pDepthStencilAttachment = depthAttachment;
	
	m_parent->m_heapRefs.push_back(depthAttachment);

	return *this;
}

VKLSubpassDescription& VKLSubpassDescription::preserveAttachment(uint32_t attachment) {
	m_preserveAttachments.push_back(attachment);

	m_desc.pPreserveAttachments = m_preserveAttachments.data();
	m_desc.preserveAttachmentCount = m_preserveAttachments.size();

	return *this;
}

VKLRenderPassCreateInfo& VKLSubpassDescription::end() {
	m_parent->m_subpassDecriptionBuffer.push_back(m_desc);

	return *m_parent;
}

VKLSubpassDescription::VKLSubpassDescription(VKLRenderPassCreateInfo* parent) : m_parent(parent) {
	memset(&m_desc, 0, sizeof(VkSubpassDescription));
	m_desc.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
	m_desc.pDepthStencilAttachment = NULL;
}

VKLSubpassDependency& VKLSubpassDependency::stages(VkPipelineStageFlags srcStage, VkPipelineStageFlags dstStage) {
	m_dependency.srcStageMask = srcStage;
	m_dependency.dstStageMask = dstStage;
	
	return *this;
}

VKLSubpassDependency& VKLSubpassDependency::access(VkAccessFlags srcAccess, VkAccessFlags dstAccess) {
	m_dependency.srcAccessMask = srcAccess;
	m_dependency.dstAccessMask = dstAccess;
	
	return *this;
}

VKLRenderPassCreateInfo& VKLSubpassDependency::end() {
	m_parent->m_subpassDependenciesBuffer.push_back(m_dependency);
	
	return *m_parent;
}

VKLSubpassDependency::VKLSubpassDependency(VKLRenderPassCreateInfo* parent, uint32_t srcSubpass, uint32_t dstSubpass, VkDependencyFlags dependencyFlags) : m_parent(parent) {
	memset(&m_dependency, 0, sizeof(VkSubpassDependency));
	
	m_dependency.dependencyFlags = dependencyFlags;
	m_dependency.srcSubpass = srcSubpass;
	m_dependency.dstSubpass = dstSubpass;
}
