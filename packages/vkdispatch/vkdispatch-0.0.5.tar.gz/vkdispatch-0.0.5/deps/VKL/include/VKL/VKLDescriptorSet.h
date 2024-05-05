#ifndef VKLDescriptorSet_h
#define VKLDescriptorSet_h

#include <VKL/VKL_base.h>

class VKLDescriptorSet : public VKLHandle<VkDescriptorSet>{
public:
	VKLDescriptorSet(const VKLPipelineLayout* layout, uint32_t set);
	
	VkDescriptorPool pool() const;
	
	//void bind(const VKLCommandBuffer* cmdBuffer) const;
	
	const VKLPipelineLayout* layout() const;
	const VKLDevice* device() const;
	uint32_t set() const;
	
	void writeImage(uint32_t binding, VkDescriptorType type, VkImageView view, VkImageLayout layout, VkSampler sampler);
	void writeBuffer(uint32_t binding, VkDescriptorType type, const VKLBuffer* buffer, VkDeviceSize offset, VkDeviceSize range);
	
	void destroy();
private:
	const VKLPipelineLayout* m_layout;
	const VKLDevice* m_device;
	
	uint32_t m_set;
	
	VkDescriptorPool m_pool;
};

#endif /* VKLDescriptorSet_h */
