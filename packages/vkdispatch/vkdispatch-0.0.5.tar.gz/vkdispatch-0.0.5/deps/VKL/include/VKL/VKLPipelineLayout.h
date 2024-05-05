#ifndef VKLPipelineLayout_h
#define VKLPipelineLayout_h

#include <VKL/VKL_base.h>

typedef enum {
	VKL_PIPELINE_TYPE_GRAPHICS = 0,
	VKL_PIPELINE_TYPE_COMPUTE = 1
} VKLPipelineType;

typedef struct {
	VkShaderModuleCreateInfo createInfo;
	VkShaderStageFlagBits stage;
	const char* entryPoint;
} VKLShaderModuleCreateInfo;

class VKLPipelineLayoutCreateInfo;

class VKLDescriptorSetLayoutCreateInfo {
public:
	VKLDescriptorSetLayoutCreateInfo& addBinding(uint32_t binding, VkDescriptorType type,
												uint32_t count, VkShaderStageFlags stage);
	VKLPipelineLayoutCreateInfo& end();
	
private:
	VKLDescriptorSetLayoutCreateInfo(VKLPipelineLayoutCreateInfo& parent);

	std::vector<VkDescriptorSetLayoutBinding> m_bindings;
	VKLPipelineLayoutCreateInfo& m_parent;

	friend class VKLPipelineLayoutCreateInfo;
	friend class VKLPipelineLayout;
};

class VKLPipelineLayoutCreateInfo : public VKLCreateInfo<VKLPipelineLayoutCreateInfo>{
public:
	VKLPipelineLayoutCreateInfo();
	
	VKLPipelineLayoutCreateInfo& device(const VKLDevice* device);
	VKLDescriptorSetLayoutCreateInfo& addDescriptorSet();
	VKLPipelineLayoutCreateInfo& addPushConstant(VkShaderStageFlags stage, uint32_t offset, uint32_t size);
	VKLPipelineLayoutCreateInfo& addShaderModule(const uint32_t* pCode, size_t codeSize,
										 VkShaderStageFlagBits stage, const char* entryPoint);
	VKLPipelineLayoutCreateInfo& addShaderModuleSource(const char* source, VkShaderStageFlagBits stage, const char* entryPoint, const char* shaderName);
private:

	std::vector<VKLShaderModuleCreateInfo> m_shaderModuleCreateInfos;
	std::vector<VkVertexInputAttributeDescription> m_vertexAttribs;
	std::vector<VkPushConstantRange> m_pushConstantRanges;
	std::vector<VKLDescriptorSetLayoutCreateInfo> m_descriptorSetLayouts;
	const VKLDevice* m_device;
	
	VKLPipelineType m_type;
	
	void addVertexAttrib(uint32_t location, uint32_t binding, VkFormat format, uint32_t offset);

	bool _validate();

	friend class VKLDescriptorSetLayoutCreateInfo;
	friend class VKLPipelineLayout;
};

class VKLPipelineLayout : public VKLHandle<VkPipelineLayout>, public VKLCreator<VKLPipelineLayoutCreateInfo>{
public:
	VKLPipelineLayout();
	VKLPipelineLayout(const VKLPipelineLayoutCreateInfo& createInfo);
	
	const std::vector<VkPipelineShaderStageCreateInfo>& getShaderStageCreateInfos() const;
	const VKLDevice* device() const;
	const VkDescriptorSetLayout* descriptorSetLayouts() const;
	
	VKLPipelineType type() const;
	VkPipelineBindPoint bindPoint() const;
private:
	const VKLDevice* m_device;
	
	VkPipelineBindPoint m_bindPoint;
	VKLPipelineType m_type;
	
	std::vector<VkPipelineShaderStageCreateInfo> m_shaderStageCreateInfos;
	
	uint32_t m_descSetCount;
	VkPushConstantRange* m_pushConstantRanges;
	VkDescriptorSetLayout* m_descriptorSetLayouts;
	
	std::vector< std::vector<VkDescriptorPoolSize> > m_descriptorPoolSizes;
	
	void _destroy();
	void _create(const VKLPipelineLayoutCreateInfo& createInfo);
	
	friend class VKLDescriptorSet;
};

#endif
