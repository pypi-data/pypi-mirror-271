#ifndef VKLCommandBuffer_h
#define VKLCommandBuffer_h

#include "VKL_base.h"

class VKLCommandBuffer : public VKLHandle<VkCommandBuffer> {
public:
	VKLCommandBuffer(const VKLQueue* queue, int count = 1);

	VkCommandPool pool() const;
	VkCommandPool* pPool() const;

	VkFence fence() const;
	VkFence* pFence() const;
	
	void bufferBarrier(VKLBuffer* buffer, VkPipelineStageFlags srcStageMask, VkPipelineStageFlags dstStageMask) const;
	
	void copyBuffer(const VKLBuffer* dst, const VKLBuffer* src, VkBufferCopy bufferCopy) const;
	void copyImage(const VKLImage* dst, const VKLImage* src, VkImageCopy imageCopy) const;
	
	void begin() const;
	void end() const;
	
	void beginRenderPass(const VKLFramebuffer& framebuffer, VkSubpassContents contents) const;
	void beginRenderPass(const VKLFramebuffer& framebuffer, VkSubpassContents contents, VkRect2D area) const;
	
	void beginRenderPass(const VKLFramebuffer* framebuffer, VkSubpassContents contents) const;
	void beginRenderPass(const VKLFramebuffer* framebuffer, VkSubpassContents contents, VkRect2D area) const;
	
	void nextSubpass(VkSubpassContents contents) const;
	void endRenderPass() const;
	
	void setViewPort(uint32_t index, uint32_t width, uint32_t height) const;
	void setViewPort(uint32_t index, uint32_t x, uint32_t y, uint32_t width, uint32_t height) const;
	void setViewPort(uint32_t index, uint32_t x, uint32_t y, uint32_t width, uint32_t height, uint32_t z, uint32_t depth) const;
	
	void setScissor(uint32_t index, uint32_t width, uint32_t height) const;
	void setScissor(uint32_t index, uint32_t x, uint32_t y, uint32_t width, uint32_t height) const;
	
	void bindVertexBuffer(const VKLBuffer& buffer, uint32_t binding, VkDeviceSize offset) const;
	void bindVertexBuffer(const VKLBuffer* buffer, uint32_t binding, VkDeviceSize offset) const;
	
	void bindPipeline(const VKLPipeline& pipeline) const;
	void bindPipeline(const VKLPipeline* pipeline) const;
	
	void bindDescriptorSet(const VKLDescriptorSet& descriptorSet) const;
	void bindDescriptorSet(const VKLDescriptorSet* descriptorSet) const;

	void pushConstants(const VKLPipeline& pipeline, VkShaderStageFlags stageFlags, uint32_t offset, uint32_t size, const void* pValues) const;
	void pushConstants(const VKLPipeline* pipeline, VkShaderStageFlags stageFlags, uint32_t offset, uint32_t size, const void* pValues) const;
	
	void draw(uint32_t vertexCount, uint32_t instanceCount, uint32_t firstVertex, uint32_t firstInstance) const;
	void dispatch(uint32_t x, uint32_t y, uint32_t z) const;

	void destroy();
//private:
	VkCommandPool m_pool;
	VkCommandBuffer* m_handles;
	VkFence* m_fences;
	int m_count;
	int m_current_index;
	
	const VKLQueue* m_queue;
	const VKLDevice* m_device;
};

#endif /* VKLCommandBuffer_h */
