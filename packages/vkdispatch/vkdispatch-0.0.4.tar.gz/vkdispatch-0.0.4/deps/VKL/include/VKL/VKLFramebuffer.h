#ifndef VKLFramebuffer_h
#define VKLFramebuffer_h

#include <VKL/VKL_base.h>

class VKLFramebufferCreateInfo : public VKLCreateInfo<VKLFramebufferCreateInfo> {
public:
	VKLFramebufferCreateInfo();
	
	VKLFramebufferCreateInfo& renderPass(const VKLRenderPass* renderPass);
	VKLFramebufferCreateInfo& addAttachment(const VKLImageView* imageView);
	VKLFramebufferCreateInfo& extent(uint32_t width, uint32_t height, uint32_t layers);
private:
	const VKLRenderPass* m_renderPass;
	std::vector<const VKLImageView*> m_attachments;
	std::vector<VkImageView> m_attachmentsBuffer;
	VkFramebufferCreateInfo m_createInfo;
	
	bool _validate();
	
	friend class VKLFramebuffer;
};

class VKLFramebuffer : public VKLHandle<VkFramebuffer>, public VKLCreator<VKLFramebufferCreateInfo>{
public:
	VKLFramebuffer();
	VKLFramebuffer(const VKLFramebufferCreateInfo& createInfo);
	
	VkExtent2D size() const;
	const VKLRenderPass* renderPass() const;
	const VkClearValue* clearValues() const;
	const std::vector<const VKLImageView*>& attachments() const;
	
	void setClearValue(VkClearValue clearValue, uint32_t index);
private:
	const VKLRenderPass* m_renderPass;
	const VKLDevice* m_device;
	
	VkExtent2D m_size;
	
	std::vector<const VKLImageView*> m_attachments;
	
	VkClearValue* m_clearValues;
	
	void _create(const VKLFramebufferCreateInfo& createInfo);
	void _destroy();
};

#endif /* VKLFramebuffer_h */
