#include <VKL/VKL.h>

VKLPipeline::VKLPipeline() : VKLCreator<VKLPipelineCreateInfo>("VKLPipeline") {
	
}

const VKLPipelineLayout* VKLPipeline::layout() const {
	return m_layout;
}

const VKLDevice* VKLPipeline::device() const {
	return m_device;
}

void VKLPipeline::_destroy() {
	m_device->vk.DestroyPipeline(m_device->handle(), m_handle, m_device->allocationCallbacks());
}

void VKLPipeline::_create(const VKLPipelineCreateInfo& createInfo) {
	m_layout = createInfo.m_layout;
	m_device = m_layout->device();
	
	if(m_layout->type() == VKL_PIPELINE_TYPE_GRAPHICS) {
		VkPipelineInputAssemblyStateCreateInfo inputAssemblyStateCreateInfo;
		memset(&inputAssemblyStateCreateInfo, 0, sizeof(VkPipelineInputAssemblyStateCreateInfo));
		inputAssemblyStateCreateInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO;
		inputAssemblyStateCreateInfo.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
		inputAssemblyStateCreateInfo.primitiveRestartEnable = VK_FALSE;

		VkViewport viewport;
		memset(&viewport, 0, sizeof(VkViewport));
		viewport.x = 0;//createInfo.m_renderPass->getRenderArea().offset.x;
		viewport.y = 0;//createInfo.m_renderPass->getRenderArea().offset.y;
		viewport.width = 800;//createInfo.m_renderPass->getRenderArea().extent.width;
		viewport.height = 600;//createInfo.m_renderPass->getRenderArea().extent.height;
		viewport.minDepth = 0;
		viewport.maxDepth = 1;

		VkRect2D scissors;
		memset(&scissors, 0, sizeof(VkRect2D));
		scissors.offset.x = 0;
		scissors.offset.y = 0;
		scissors.extent.width = 800;//createInfo.m_renderTarget->getRenderArea().extent.width;
		scissors.extent.height = 600;//createInfo.m_renderTarget->getRenderArea().extent.height;

		VkPipelineViewportStateCreateInfo viewportState;
		memset(&viewportState, 0, sizeof(VkPipelineViewportStateCreateInfo));
		viewportState.sType = VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO;
		viewportState.viewportCount = 1;
		viewportState.pViewports = &viewport;
		viewportState.scissorCount = 1;
		viewportState.pScissors = &scissors;

		VkPipelineRasterizationStateCreateInfo rasterizationState;
		memset(&rasterizationState, 0, sizeof(VkPipelineRasterizationStateCreateInfo));
		rasterizationState.sType = VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO;
		rasterizationState.depthClampEnable = VK_FALSE;
		rasterizationState.rasterizerDiscardEnable = VK_FALSE;
		rasterizationState.polygonMode = VK_POLYGON_MODE_FILL;
		rasterizationState.cullMode = VK_CULL_MODE_FRONT_BIT;
		rasterizationState.frontFace = VK_FRONT_FACE_COUNTER_CLOCKWISE;
		rasterizationState.depthBiasEnable = VK_FALSE;
		rasterizationState.depthBiasConstantFactor = 0;
		rasterizationState.depthBiasClamp = 0;
		rasterizationState.depthBiasSlopeFactor = 0;
		rasterizationState.lineWidth = 1;

		VkPipelineMultisampleStateCreateInfo multisampleState;
		memset(&multisampleState, 0, sizeof(VkPipelineMultisampleStateCreateInfo));
		multisampleState.sType = VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO;
		multisampleState.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
		multisampleState.sampleShadingEnable = VK_FALSE;
		multisampleState.minSampleShading = 0;
		multisampleState.pSampleMask = NULL;
		multisampleState.alphaToCoverageEnable = VK_FALSE;
		multisampleState.alphaToOneEnable = VK_FALSE;

		VkStencilOpState noOPStencilState;
		memset(&noOPStencilState, 0, sizeof(VkStencilOpState));
		noOPStencilState.failOp = VK_STENCIL_OP_KEEP;
		noOPStencilState.passOp = VK_STENCIL_OP_KEEP;
		noOPStencilState.depthFailOp = VK_STENCIL_OP_KEEP;
		noOPStencilState.compareOp = VK_COMPARE_OP_ALWAYS;
		noOPStencilState.compareMask = 0;
		noOPStencilState.writeMask = 0;
		noOPStencilState.reference = 0;

		VkPipelineDepthStencilStateCreateInfo depthState;
		memset(&depthState, 0, sizeof(VkPipelineDepthStencilStateCreateInfo));
		depthState.sType = VK_STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO;
		depthState.depthTestEnable = VK_TRUE;
		depthState.depthWriteEnable = VK_TRUE;
		depthState.depthCompareOp = VK_COMPARE_OP_LESS_OR_EQUAL;
		depthState.depthBoundsTestEnable = VK_FALSE;
		depthState.stencilTestEnable = VK_FALSE;
		depthState.front = noOPStencilState;
		depthState.back = noOPStencilState;
		depthState.minDepthBounds = 0;
		depthState.maxDepthBounds = 0;

		VkPipelineColorBlendAttachmentState colorBlendAttachmentState;
		memset(&colorBlendAttachmentState, 0, sizeof(VkPipelineColorBlendAttachmentState));
		colorBlendAttachmentState.blendEnable = VK_TRUE;
		colorBlendAttachmentState.srcColorBlendFactor = VK_BLEND_FACTOR_ONE; // Use source color (fragment shader output)
		colorBlendAttachmentState.dstColorBlendFactor = VK_BLEND_FACTOR_ONE; // Add to destination color (existing content in the backbuffer)
		colorBlendAttachmentState.colorBlendOp = VK_BLEND_OP_ADD; // Add source and destination colors
		colorBlendAttachmentState.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
		colorBlendAttachmentState.dstAlphaBlendFactor = VK_BLEND_FACTOR_ZERO; // Not relevant for R32_SFLOAT
		colorBlendAttachmentState.alphaBlendOp = VK_BLEND_OP_ADD;
		colorBlendAttachmentState.colorWriteMask = VK_COLOR_COMPONENT_R_BIT; // Only write to the red component for R32_SFLOAT
		//colorBlendAttachmentState.srcColorBlendFactor = VK_BLEND_FACTOR_SRC_COLOR;
		//colorBlendAttachmentState.dstColorBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_DST_COLOR;
		//colorBlendAttachmentState.colorBlendOp = VK_BLEND_OP_ADD;
		//colorBlendAttachmentState.srcAlphaBlendFactor = VK_BLEND_FACTOR_ZERO;
		//colorBlendAttachmentState.dstAlphaBlendFactor = VK_BLEND_FACTOR_ZERO;
		//colorBlendAttachmentState.alphaBlendOp = VK_BLEND_OP_ADD;
		//colorBlendAttachmentState.colorWriteMask = 0xf;
		
		VkPipelineColorBlendAttachmentState* colorBlendAttachmentStates = (VkPipelineColorBlendAttachmentState*)malloc(sizeof(VkPipelineColorBlendAttachmentState)
																													   * createInfo.m_renderPass->m_subpassColorAttachmentCounts[createInfo.m_subpass]);
		
		for(int i = 0; i < createInfo.m_renderPass->m_subpassColorAttachmentCounts[createInfo.m_subpass]; i++) {
			colorBlendAttachmentStates[i] = colorBlendAttachmentState;
		}
		
		VkPipelineColorBlendStateCreateInfo colorBlendState;
		memset(&colorBlendState, 0, sizeof(VkPipelineColorBlendStateCreateInfo));
		colorBlendState.sType = VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO;
		colorBlendState.logicOpEnable = VK_FALSE;
		colorBlendState.logicOp = VK_LOGIC_OP_CLEAR;
		colorBlendState.attachmentCount = createInfo.m_renderPass->m_subpassColorAttachmentCounts[createInfo.m_subpass];
		colorBlendState.pAttachments = colorBlendAttachmentStates;
		colorBlendState.blendConstants[0] = 0.0;
		colorBlendState.blendConstants[1] = 0.0;
		colorBlendState.blendConstants[2] = 0.0;
		colorBlendState.blendConstants[3] = 0.0;
		
		VkDynamicState dynamicState[2] = { VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR };
		VkPipelineDynamicStateCreateInfo dynamicStateCreateInfo;
		memset(&dynamicStateCreateInfo, 0, sizeof(VkPipelineDynamicStateCreateInfo));
		dynamicStateCreateInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO;
		dynamicStateCreateInfo.dynamicStateCount = 2;
		dynamicStateCreateInfo.pDynamicStates = dynamicState;

		VkGraphicsPipelineCreateInfo pipelineCreateInfo;
		memset(&pipelineCreateInfo, 0, sizeof(VkGraphicsPipelineCreateInfo));
		pipelineCreateInfo.sType = VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO;
		pipelineCreateInfo.stageCount = createInfo.m_layout->getShaderStageCreateInfos().size();
		pipelineCreateInfo.pStages = createInfo.m_layout->getShaderStageCreateInfos().data();
		pipelineCreateInfo.pVertexInputState = &createInfo.vertexInput.m_createInfo;
		pipelineCreateInfo.pInputAssemblyState = &inputAssemblyStateCreateInfo;
		pipelineCreateInfo.pTessellationState = NULL;
		pipelineCreateInfo.pViewportState = &viewportState;
		pipelineCreateInfo.pRasterizationState = &rasterizationState;
		pipelineCreateInfo.pMultisampleState = &multisampleState;
		pipelineCreateInfo.pDepthStencilState = &depthState;
		pipelineCreateInfo.pColorBlendState = &colorBlendState;
		pipelineCreateInfo.pDynamicState = &dynamicStateCreateInfo;
		pipelineCreateInfo.layout = createInfo.m_layout->handle();
		pipelineCreateInfo.renderPass = createInfo.m_renderPass->handle();
		pipelineCreateInfo.subpass = createInfo.m_subpass;
		pipelineCreateInfo.basePipelineHandle = NULL;
		pipelineCreateInfo.basePipelineIndex = 0;
		
		VK_CALL(m_device->vk.CreateGraphicsPipelines(m_device->handle(), (VkPipelineCache)VK_NULL_HANDLE, 1, &pipelineCreateInfo, m_device->allocationCallbacks(), &m_handle));
		
		free(colorBlendAttachmentStates);
	} else if (m_layout->type() == VKL_PIPELINE_TYPE_COMPUTE) {
		VkComputePipelineCreateInfo pipelineCreateInfo;
		memset(&pipelineCreateInfo, 0, sizeof(VkComputePipelineCreateInfo));
		pipelineCreateInfo.sType = VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO;
		pipelineCreateInfo.layout = m_layout->handle();
		pipelineCreateInfo.stage = m_layout->getShaderStageCreateInfos()[0];
		
		VK_CALL(m_device->vk.CreateComputePipelines(m_device->handle(), (VkPipelineCache)VK_NULL_HANDLE, 1, &pipelineCreateInfo, m_device->allocationCallbacks(), &m_handle));
	}
	
}

VKLPipelineCreateInfo::VKLPipelineCreateInfo() : vertexInput(*this) {
	m_layout = NULL;
	m_renderPass = NULL;
	m_subpass = 0;
}

VKLPipelineCreateInfo& VKLPipelineCreateInfo::layout(const VKLPipelineLayout* layout) {
	m_layout = layout;
	
	return invalidate();
}

VKLPipelineCreateInfo& VKLPipelineCreateInfo::renderPass(const VKLRenderPass* renderPass, uint32_t subpass) {
	m_renderPass = renderPass;
	m_subpass = subpass;
	
	return invalidate();
}

bool VKLPipelineCreateInfo::_validate() {
	if(m_layout == NULL) {
		printf("VKL Validation Error: VKLPipelineCreateInfo::layout is not set!\n");
		return false;
	}

	if(m_layout->type() == VKL_PIPELINE_TYPE_GRAPHICS) {
		if (m_renderPass == NULL) {
			printf("VKL Validation Error: VKLPipelineCreateInfo::renderPass is not set!\n");
			return false;
		}

		if (!vertexInput.validate()) {
			printf("VKL Validation Error: VKLPipelineCreateInfo::vertexInput is not valid!\n");
			return false;
		}
	}
	
	return true;
}

VKLVertexInputBindingDesc& VKLPipelineVertexInputStateCreateInfo::addBinding(uint32_t binding, uint32_t stride) {
	m_vertexInputBindings.push_back(VKLVertexInputBindingDesc(binding, stride, this));

	return m_vertexInputBindings.back();
}

VKLPipelineCreateInfo& VKLPipelineVertexInputStateCreateInfo::end() {
	return m_parent;
}

VKLPipelineVertexInputStateCreateInfo::VKLPipelineVertexInputStateCreateInfo(VKLPipelineCreateInfo& parent) : m_parent(parent) {
	m_vertexInputBindingsBuffer = NULL;

	memset(&m_createInfo, 0, sizeof(VkPipelineVertexInputStateCreateInfo));
	m_createInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO;
	m_createInfo.pNext = NULL;
	m_createInfo.flags = 0;
	m_createInfo.pVertexAttributeDescriptions = NULL;
	m_createInfo.vertexAttributeDescriptionCount = 0;
	m_createInfo.pVertexBindingDescriptions = NULL;
	m_createInfo.vertexBindingDescriptionCount = 0;
}

void VKLPipelineVertexInputStateCreateInfo::addVertexAttrib(uint32_t location, uint32_t binding, VkFormat format, uint32_t offset) {
	VkVertexInputAttributeDescription result;
	result.binding = binding;
	result.format = format;
	result.location = location;
	result.offset = offset;

	m_vertexAttributes.push_back(result);
}

bool VKLPipelineVertexInputStateCreateInfo::validate() {
	if (m_vertexInputBindingsBuffer != NULL) {
		free(m_vertexInputBindingsBuffer);
	}

	m_vertexInputBindingsBuffer = (VkVertexInputBindingDescription*)malloc(sizeof(VkVertexInputBindingDescription) * m_vertexInputBindings.size());
	
	for (int i = 0; i < m_vertexInputBindings.size(); i++) {
		m_vertexInputBindingsBuffer[i] = m_vertexInputBindings[i].m_desc;
	}

	m_createInfo.pVertexAttributeDescriptions = m_vertexAttributes.data();
	m_createInfo.vertexAttributeDescriptionCount = m_vertexAttributes.size();
	m_createInfo.pVertexBindingDescriptions = m_vertexInputBindingsBuffer;
	m_createInfo.vertexBindingDescriptionCount = m_vertexInputBindings.size();

	return true;
}

VKLVertexInputBindingDesc::VKLVertexInputBindingDesc(uint32_t binding, uint32_t stride, VKLPipelineVertexInputStateCreateInfo* parent) {
	memset(&m_desc, 0, sizeof(VkVertexInputBindingDescription));
	m_desc.binding = binding;
	m_desc.stride = stride;
	m_desc.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;

	m_parent = parent;
}

VKLVertexInputBindingDesc& VKLVertexInputBindingDesc::inputRate(VkVertexInputRate inputRate) {
	m_desc.inputRate = inputRate;

	return *this;
}

VKLVertexInputBindingDesc& VKLVertexInputBindingDesc::addAttrib(uint32_t location, VkFormat format, uint32_t offset) {
	m_parent->addVertexAttrib(location, m_desc.binding, format, offset);

	return *this;
}

VKLPipelineVertexInputStateCreateInfo& VKLVertexInputBindingDesc::end() {
	return *m_parent;
}
