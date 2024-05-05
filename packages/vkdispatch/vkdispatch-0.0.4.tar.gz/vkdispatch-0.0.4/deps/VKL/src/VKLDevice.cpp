#include <VKL/VKL.h>

VKLDevice::VKLDevice() : VKLCreator<VKLDeviceCreateInfo>("VKLDevice") {
	m_instance = NULL;
	m_physicalDevice = NULL;
	m_allocationCallbacks = NULL;

	memset(&vk, 0, sizeof(VKLDevicePFNS));
}


VKLDevice::VKLDevice(const VKLDeviceCreateInfo& createInfo) : VKLCreator<VKLDeviceCreateInfo>("VKLDevice")  {
	m_instance = NULL;
	m_physicalDevice = NULL;
	m_allocationCallbacks = NULL;

	memset(&vk, 0, sizeof(VKLDevicePFNS));

	create(createInfo);
}

void VKLDevice::_create(const VKLDeviceCreateInfo& createInfo) {
	LOG_INFO("Creating device");
	
	m_instance = createInfo.m_instance;
	m_physicalDevice = createInfo.m_physicalDevice;
	m_allocationCallbacks = m_instance->allocationCallbacks();

	vk.CreateDevice = (PFN_vkCreateDevice)m_instance->procAddr("vkCreateDevice");
	vk.GetDeviceProcAddr = (PFN_vkGetDeviceProcAddr)m_instance->procAddr("vkGetDeviceProcAddr");

	LOG_INFO("Calling vkCreateDevice");

	VK_CALL(vk.CreateDevice(m_physicalDevice->handle(), &createInfo.m_createInfo, m_instance->allocationCallbacks(), &m_handle));

	LOG_INFO("Device created");

	vk.DestroyDevice = (PFN_vkDestroyDevice)procAddr("vkDestroyDevice");
	vk.GetDeviceQueue = (PFN_vkGetDeviceQueue)procAddr("vkGetDeviceQueue");
	vk.QueueSubmit = (PFN_vkQueueSubmit)procAddr("vkQueueSubmit");
	vk.QueueWaitIdle = (PFN_vkQueueWaitIdle)procAddr("vkQueueWaitIdle");
	vk.DeviceWaitIdle = (PFN_vkDeviceWaitIdle)procAddr("vkDeviceWaitIdle");
	vk.AllocateMemory = (PFN_vkAllocateMemory)procAddr("vkAllocateMemory");
	vk.FreeMemory = (PFN_vkFreeMemory)procAddr("vkFreeMemory");
	vk.MapMemory = (PFN_vkMapMemory)procAddr("vkMapMemory");
	vk.UnmapMemory = (PFN_vkUnmapMemory)procAddr("vkUnmapMemory");
	vk.FlushMappedMemoryRanges = (PFN_vkFlushMappedMemoryRanges)procAddr("vkFlushMappedMemoryRanges");
	vk.InvalidateMappedMemoryRanges = (PFN_vkInvalidateMappedMemoryRanges)procAddr("vkInvalidateMappedMemoryRanges");
	vk.GetDeviceMemoryCommitment = (PFN_vkGetDeviceMemoryCommitment)procAddr("vkGetDeviceMemoryCommitment");
	vk.BindBufferMemory = (PFN_vkBindBufferMemory)procAddr("vkBindBufferMemory");
	vk.BindImageMemory = (PFN_vkBindImageMemory)procAddr("vkBindImageMemory");
	vk.GetBufferMemoryRequirements = (PFN_vkGetBufferMemoryRequirements)procAddr("vkGetBufferMemoryRequirements");
	vk.GetImageMemoryRequirements = (PFN_vkGetImageMemoryRequirements)procAddr("vkGetImageMemoryRequirements");
	vk.GetImageSparseMemoryRequirements = (PFN_vkGetImageSparseMemoryRequirements)procAddr("vkGetImageSparseMemoryRequirements");
	vk.GetPhysicalDeviceSparseImageFormatProperties = (PFN_vkGetPhysicalDeviceSparseImageFormatProperties)procAddr("vkGetPhysicalDeviceSparseImageFormatProperties");
	vk.QueueBindSparse = (PFN_vkQueueBindSparse)procAddr("vkQueueBindSparse");
	vk.CreateFence = (PFN_vkCreateFence)procAddr("vkCreateFence");
	vk.DestroyFence = (PFN_vkDestroyFence)procAddr("vkDestroyFence");
	vk.ResetFences = (PFN_vkResetFences)procAddr("vkResetFences");
	vk.GetFenceStatus = (PFN_vkGetFenceStatus)procAddr("vkGetFenceStatus");
	vk.WaitForFences = (PFN_vkWaitForFences)procAddr("vkWaitForFences");
	vk.CreateSemaphore = (PFN_vkCreateSemaphore)procAddr("vkCreateSemaphore");
	vk.DestroySemaphore = (PFN_vkDestroySemaphore)procAddr("vkDestroySemaphore");
	vk.CreateEvent = (PFN_vkCreateEvent)procAddr("vkCreateEvent");
	vk.DestroyEvent = (PFN_vkDestroyEvent)procAddr("vkDestroyEvent");
	vk.GetEventStatus = (PFN_vkGetEventStatus)procAddr("vkGetEventStatus");
	vk.SetEvent = (PFN_vkSetEvent)procAddr("vkSetEvent");
	vk.ResetEvent = (PFN_vkResetEvent)procAddr("vkResetEvent");
	vk.CreateQueryPool = (PFN_vkCreateQueryPool)procAddr("vkCreateQueryPool");
	vk.DestroyQueryPool = (PFN_vkDestroyQueryPool)procAddr("vkDestroyQueryPool");
	vk.GetQueryPoolResults = (PFN_vkGetQueryPoolResults)procAddr("vkGetQueryPoolResults");
	vk.CreateBuffer = (PFN_vkCreateBuffer)procAddr("vkCreateBuffer");
	vk.DestroyBuffer = (PFN_vkDestroyBuffer)procAddr("vkDestroyBuffer");
	vk.CreateBufferView = (PFN_vkCreateBufferView)procAddr("vkCreateBufferView");
	vk.DestroyBufferView = (PFN_vkDestroyBufferView)procAddr("vkDestroyBufferView");
	vk.CreateImage = (PFN_vkCreateImage)procAddr("vkCreateImage");
	vk.DestroyImage = (PFN_vkDestroyImage)procAddr("vkDestroyImage");
	vk.GetImageSubresourceLayout = (PFN_vkGetImageSubresourceLayout)procAddr("vkGetImageSubresourceLayout");
	vk.CreateImageView = (PFN_vkCreateImageView)procAddr("vkCreateImageView");
	vk.DestroyImageView = (PFN_vkDestroyImageView)procAddr("vkDestroyImageView");
	vk.CreateShaderModule = (PFN_vkCreateShaderModule)procAddr("vkCreateShaderModule");
	vk.DestroyShaderModule = (PFN_vkDestroyShaderModule)procAddr("vkDestroyShaderModule");
	vk.CreatePipelineCache = (PFN_vkCreatePipelineCache)procAddr("vkCreatePipelineCache");
	vk.DestroyPipelineCache = (PFN_vkDestroyPipelineCache)procAddr("vkDestroyPipelineCache");
	vk.GetPipelineCacheData = (PFN_vkGetPipelineCacheData)procAddr("vkGetPipelineCacheData");
	vk.MergePipelineCaches = (PFN_vkMergePipelineCaches)procAddr("vkMergePipelineCaches");
	vk.CreateGraphicsPipelines = (PFN_vkCreateGraphicsPipelines)procAddr("vkCreateGraphicsPipelines");
	vk.CreateComputePipelines = (PFN_vkCreateComputePipelines)procAddr("vkCreateComputePipelines");
	vk.DestroyPipeline = (PFN_vkDestroyPipeline)procAddr("vkDestroyPipeline");
	vk.CreatePipelineLayout = (PFN_vkCreatePipelineLayout)procAddr("vkCreatePipelineLayout");
	vk.DestroyPipelineLayout = (PFN_vkDestroyPipelineLayout)procAddr("vkDestroyPipelineLayout");
	vk.CreateSampler = (PFN_vkCreateSampler)procAddr("vkCreateSampler");
	vk.DestroySampler = (PFN_vkDestroySampler)procAddr("vkDestroySampler");
	vk.CreateDescriptorSetLayout = (PFN_vkCreateDescriptorSetLayout)procAddr("vkCreateDescriptorSetLayout");
	vk.DestroyDescriptorSetLayout = (PFN_vkDestroyDescriptorSetLayout)procAddr("vkDestroyDescriptorSetLayout");
	vk.CreateDescriptorPool = (PFN_vkCreateDescriptorPool)procAddr("vkCreateDescriptorPool");
	vk.DestroyDescriptorPool = (PFN_vkDestroyDescriptorPool)procAddr("vkDestroyDescriptorPool");
	vk.ResetDescriptorPool = (PFN_vkResetDescriptorPool)procAddr("vkResetDescriptorPool");
	vk.AllocateDescriptorSets = (PFN_vkAllocateDescriptorSets)procAddr("vkAllocateDescriptorSets");
	vk.FreeDescriptorSets = (PFN_vkFreeDescriptorSets)procAddr("vkFreeDescriptorSets");
	vk.UpdateDescriptorSets = (PFN_vkUpdateDescriptorSets)procAddr("vkUpdateDescriptorSets");
	vk.CreateFramebuffer = (PFN_vkCreateFramebuffer)procAddr("vkCreateFramebuffer");
	vk.DestroyFramebuffer = (PFN_vkDestroyFramebuffer)procAddr("vkDestroyFramebuffer");
	vk.CreateRenderPass = (PFN_vkCreateRenderPass)procAddr("vkCreateRenderPass");
	vk.DestroyRenderPass = (PFN_vkDestroyRenderPass)procAddr("vkDestroyRenderPass");
	vk.GetRenderAreaGranularity = (PFN_vkGetRenderAreaGranularity)procAddr("vkGetRenderAreaGranularity");
	vk.CreateCommandPool = (PFN_vkCreateCommandPool)procAddr("vkCreateCommandPool");
	vk.DestroyCommandPool = (PFN_vkDestroyCommandPool)procAddr("vkDestroyCommandPool");
	vk.ResetCommandPool = (PFN_vkResetCommandPool)procAddr("vkResetCommandPool");
	vk.AllocateCommandBuffers = (PFN_vkAllocateCommandBuffers)procAddr("vkAllocateCommandBuffers");
	vk.FreeCommandBuffers = (PFN_vkFreeCommandBuffers)procAddr("vkFreeCommandBuffers");
	vk.BeginCommandBuffer = (PFN_vkBeginCommandBuffer)procAddr("vkBeginCommandBuffer");
	vk.EndCommandBuffer = (PFN_vkEndCommandBuffer)procAddr("vkEndCommandBuffer");
	vk.ResetCommandBuffer = (PFN_vkResetCommandBuffer)procAddr("vkResetCommandBuffer");
	vk.CmdBindPipeline = (PFN_vkCmdBindPipeline)procAddr("vkCmdBindPipeline");
	vk.CmdSetViewport = (PFN_vkCmdSetViewport)procAddr("vkCmdSetViewport");
	vk.CmdSetScissor = (PFN_vkCmdSetScissor)procAddr("vkCmdSetScissor");
	vk.CmdSetLineWidth = (PFN_vkCmdSetLineWidth)procAddr("vkCmdSetLineWidth");
	vk.CmdSetDepthBias = (PFN_vkCmdSetDepthBias)procAddr("vkCmdSetDepthBias");
	vk.CmdSetBlendConstants = (PFN_vkCmdSetBlendConstants)procAddr("vkCmdSetBlendConstants");
	vk.CmdSetDepthBounds = (PFN_vkCmdSetDepthBounds)procAddr("vkCmdSetDepthBounds");
	vk.CmdSetStencilCompareMask = (PFN_vkCmdSetStencilCompareMask)procAddr("vkCmdSetStencilCompareMask");
	vk.CmdSetStencilWriteMask = (PFN_vkCmdSetStencilWriteMask)procAddr("vkCmdSetStencilWriteMask");
	vk.CmdSetStencilReference = (PFN_vkCmdSetStencilReference)procAddr("vkCmdSetStencilReference");
	vk.CmdBindDescriptorSets = (PFN_vkCmdBindDescriptorSets)procAddr("vkCmdBindDescriptorSets");
	vk.CmdBindIndexBuffer = (PFN_vkCmdBindIndexBuffer)procAddr("vkCmdBindIndexBuffer");
	vk.CmdBindVertexBuffers = (PFN_vkCmdBindVertexBuffers)procAddr("vkCmdBindVertexBuffers");
	vk.CmdDraw = (PFN_vkCmdDraw)procAddr("vkCmdDraw");
	vk.CmdDrawIndexed = (PFN_vkCmdDrawIndexed)procAddr("vkCmdDrawIndexed");
	vk.CmdDrawIndirect = (PFN_vkCmdDrawIndirect)procAddr("vkCmdDrawIndirect");
	vk.CmdDrawIndexedIndirect = (PFN_vkCmdDrawIndexedIndirect)procAddr("vkCmdDrawIndexedIndirect");
	vk.CmdDispatch = (PFN_vkCmdDispatch)procAddr("vkCmdDispatch");
	vk.CmdDispatchIndirect = (PFN_vkCmdDispatchIndirect)procAddr("vkCmdDispatchIndirect");
	vk.CmdCopyBuffer = (PFN_vkCmdCopyBuffer)procAddr("vkCmdCopyBuffer");
	vk.CmdCopyImage = (PFN_vkCmdCopyImage)procAddr("vkCmdCopyImage");
	vk.CmdBlitImage = (PFN_vkCmdBlitImage)procAddr("vkCmdBlitImage");
	vk.CmdCopyBufferToImage = (PFN_vkCmdCopyBufferToImage)procAddr("vkCmdCopyBufferToImage");
	vk.CmdCopyImageToBuffer = (PFN_vkCmdCopyImageToBuffer)procAddr("vkCmdCopyImageToBuffer");
	vk.CmdUpdateBuffer = (PFN_vkCmdUpdateBuffer)procAddr("vkCmdUpdateBuffer");
	vk.CmdFillBuffer = (PFN_vkCmdFillBuffer)procAddr("vkCmdFillBuffer");
	vk.CmdClearColorImage = (PFN_vkCmdClearColorImage)procAddr("vkCmdClearColorImage");
	vk.CmdClearDepthStencilImage = (PFN_vkCmdClearDepthStencilImage)procAddr("vkCmdClearDepthStencilImage");
	vk.CmdClearAttachments = (PFN_vkCmdClearAttachments)procAddr("vkCmdClearAttachments");
	vk.CmdResolveImage = (PFN_vkCmdResolveImage)procAddr("vkCmdResolveImage");
	vk.CmdSetEvent = (PFN_vkCmdSetEvent)procAddr("vkCmdSetEvent");
	vk.CmdResetEvent = (PFN_vkCmdResetEvent)procAddr("vkCmdResetEvent");
	vk.CmdWaitEvents = (PFN_vkCmdWaitEvents)procAddr("vkCmdWaitEvents");
	vk.CmdPipelineBarrier = (PFN_vkCmdPipelineBarrier)procAddr("vkCmdPipelineBarrier");
	vk.CmdBeginQuery = (PFN_vkCmdBeginQuery)procAddr("vkCmdBeginQuery");
	vk.CmdEndQuery = (PFN_vkCmdEndQuery)procAddr("vkCmdEndQuery");
	vk.CmdResetQueryPool = (PFN_vkCmdResetQueryPool)procAddr("vkCmdResetQueryPool");
	vk.CmdWriteTimestamp = (PFN_vkCmdWriteTimestamp)procAddr("vkCmdWriteTimestamp");
	vk.CmdCopyQueryPoolResults = (PFN_vkCmdCopyQueryPoolResults)procAddr("vkCmdCopyQueryPoolResults");
	vk.CmdPushConstants = (PFN_vkCmdPushConstants)procAddr("vkCmdPushConstants");
	vk.CmdBeginRenderPass = (PFN_vkCmdBeginRenderPass)procAddr("vkCmdBeginRenderPass");
	vk.CmdNextSubpass = (PFN_vkCmdNextSubpass)procAddr("vkCmdNextSubpass");
	vk.CmdEndRenderPass = (PFN_vkCmdEndRenderPass)procAddr("vkCmdEndRenderPass");
	vk.CmdExecuteCommands = (PFN_vkCmdExecuteCommands)procAddr("vkCmdExecuteCommands");

	vk.CreateSwapchainKHR = (PFN_vkCreateSwapchainKHR)procAddr("vkCreateSwapchainKHR");
	vk.DestroySwapchainKHR = (PFN_vkDestroySwapchainKHR)procAddr("vkDestroySwapchainKHR");
	vk.GetSwapchainImagesKHR = (PFN_vkGetSwapchainImagesKHR)procAddr("vkGetSwapchainImagesKHR");
	vk.AcquireNextImageKHR = (PFN_vkAcquireNextImageKHR)procAddr("vkAcquireNextImageKHR");
	vk.QueuePresentKHR = (PFN_vkQueuePresentKHR)procAddr("vkQueuePresentKHR");

	vk.GetMemoryFdKHR = (PFN_vkGetMemoryFdKHR)procAddr("vkGetMemoryFdKHR");
	vk.GetSemaphoreFdKHR = (PFN_vkGetSemaphoreFdKHR)procAddr("vkGetSemaphoreFdKHR");

	LOG_INFO("Device functions loaded");

	uint32_t* queueFamilyCurrentIndicies = (uint32_t*)malloc(sizeof(uint32_t) * physical()->getQueueFamilyProperties().size());
	memset(queueFamilyCurrentIndicies, 0, sizeof(uint32_t) * physical()->getQueueFamilyProperties().size());
	
	for(int i = 0; i < VKL_QUEUE_TYPE_COUNT; i++) {
		for(int j = 0; j < createInfo.m_queueTypeIndicies[i].size(); j++) {
			VKLQueueLocation queueLocation = createInfo.m_queueTypeIndicies[i][j];
			
			VkQueue queue = VK_NULL_HANDLE;
			vk.GetDeviceQueue(m_handle, queueLocation.familyIndex, queueLocation.localIndex, &queue);

			LOG_INFO("Created queue: %d %d %p", queueLocation.familyIndex, queueLocation.localIndex, queue);
			
			m_queues[i].push_back(VKLQueue());
			m_queues[i].back().init(this, queue, queueLocation.familyIndex);
		}
	}
	
	free(queueFamilyCurrentIndicies);

	LOG_INFO("Queues created");

	VmaVulkanFunctions vmaVulkanFunctions = {};
	vmaVulkanFunctions.vkGetInstanceProcAddr = vkGetInstanceProcAddr;
	vmaVulkanFunctions.vkGetDeviceProcAddr = vkGetDeviceProcAddr;

	VmaAllocatorCreateInfo allocatorCreateInfo = {};
	allocatorCreateInfo.vulkanApiVersion = VK_API_VERSION_1_2;
	allocatorCreateInfo.physicalDevice = m_physicalDevice->handle();
	allocatorCreateInfo.device = m_handle;
	allocatorCreateInfo.instance = m_instance->handle();
	allocatorCreateInfo.pVulkanFunctions = &vmaVulkanFunctions;
	
	VK_CALL(vmaCreateAllocator(&allocatorCreateInfo, &m_allocator));

	LOG_INFO("Allocator created");
}

const VkAllocationCallbacks* VKLDevice::allocationCallbacks() const {
	return m_allocationCallbacks;
}

PFN_vkVoidFunction VKLDevice::procAddr(const char* name) const {
	return vk.GetDeviceProcAddr(m_handle, name);
}

const VKLPhysicalDevice* VKLDevice::physical() const {
	return m_physicalDevice;
}

const VmaAllocator& VKLDevice::allocatorVMA() const {
	return m_allocator;
}

const VKLQueue* VKLDevice::getQueue(VKLQueueType type, uint32_t queueIndex) const {
	return &m_queues[type][queueIndex];
}

VkFence VKLDevice::createFence(VkFenceCreateFlags flags) const {
	VkFenceCreateInfo fenceCreateInfo;
	fenceCreateInfo.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
	fenceCreateInfo.pNext = NULL;
	fenceCreateInfo.flags = flags;
	
	VkFence result;
	VK_CALL(vk.CreateFence(m_handle, &fenceCreateInfo, m_allocationCallbacks, &result));
	return result;
}

void VKLDevice::waitForFence(VkFence fence) const {
	VK_CALL(vk.WaitForFences(m_handle, 1, &fence, VK_TRUE, UINT64_MAX));
}

void VKLDevice::resetFence(VkFence fence) const {
	VK_CALL(vk.ResetFences(m_handle, 1, &fence));
}

void VKLDevice::destroyFence(VkFence fence) const {
	vk.DestroyFence(m_handle, fence, m_allocationCallbacks);
}

VkSemaphore VKLDevice::createSemaphore() const {
	VkSemaphoreCreateInfo semaphoreCreateInfo;
	semaphoreCreateInfo.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
	semaphoreCreateInfo.pNext = NULL;
	semaphoreCreateInfo.flags = 0;
	
	VkSemaphore result;
	VK_CALL(vk.CreateSemaphore(m_handle, &semaphoreCreateInfo, m_allocationCallbacks, &result));
	
	return result;
}

void VKLDevice::destroySempahore(VkSemaphore semaphore) const {
	vk.DestroySemaphore(m_handle, semaphore, m_allocationCallbacks);
}

VkDeviceMemory VKLDevice::allocateMemory(VkMemoryRequirements memoryRequirements, VkMemoryPropertyFlags desiredMemoryFlags, void* pNext) const {
	VkMemoryAllocateInfo memoryAllocateInfo;
	memoryAllocateInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
	memoryAllocateInfo.pNext = pNext;
	memoryAllocateInfo.allocationSize = memoryRequirements.size;

	memoryAllocateInfo.memoryTypeIndex = -1;

	uint32_t memoryTypeBits = memoryRequirements.memoryTypeBits;
	for (uint32_t i = 0; i < 32; ++i) {
		VkMemoryType memoryType = m_physicalDevice->getMemoryProperties().memoryTypes[i];
		if (memoryTypeBits & 1) {
			if ((memoryType.propertyFlags & desiredMemoryFlags) == desiredMemoryFlags) {
				memoryAllocateInfo.memoryTypeIndex = i;
				break;
			}
		}
		memoryTypeBits = memoryTypeBits >> 1;
	}

	if(memoryAllocateInfo.memoryTypeIndex == -1) {
		printf("Error allocating memory!!!\n");
		return (VkDeviceMemory)VK_NULL_HANDLE;
	}

	VkDeviceMemory memory;
	VK_CALL(vk.AllocateMemory(m_handle, &memoryAllocateInfo, m_allocationCallbacks, &memory));

	return memory;
}

void VKLDevice::_destroy() {
	for (int i = 0; i < VKL_QUEUE_TYPE_COUNT; i++) {
		for (int j = 0; j < m_queues[i].size(); j++) {
			m_queues[i][j].destroy();
		}
	}

	vmaDestroyAllocator(m_allocator);
	vk.DestroyDevice(m_handle, allocationCallbacks());
}

VKLDeviceCreateInfo::VKLDeviceCreateInfo() {
	m_physicalDevice = NULL;
	m_instance = NULL;
	
	m_queueTypeCounts[0] = 0;
	m_queueTypeCounts[1] = 0;
	m_queueTypeCounts[2] = 0;
	m_queueTypeCounts[3] = 0;
	
	memset(&m_features, 0, sizeof(VkPhysicalDeviceFeatures2));
	memset(&m_createInfo, 0, sizeof(VkDeviceCreateInfo));
	
	m_createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
	m_createInfo.pNext = NULL;
	m_createInfo.flags = 0;
	m_createInfo.pEnabledFeatures = NULL;
}

VKLDeviceCreateInfo& VKLDeviceCreateInfo::physicalDevice(const VKLPhysicalDevice* physicalDevice) {
	m_physicalDevice = physicalDevice;
	
	m_instance = physicalDevice->instance();
	
	m_features = physicalDevice->getFeatures2();
	
	m_createInfo.enabledLayerCount = m_instance->getLayers().size();
	m_createInfo.ppEnabledLayerNames = m_instance->getLayers().data();

	m_createInfo.pNext = &m_features;
	
	return invalidate();
}

VKLDeviceCreateInfo& VKLDeviceCreateInfo::queueTypeCount(VKLQueueType type, uint32_t count) {
	m_queueTypeCounts[type] = count;
	
	return invalidate();
}

VKLDeviceCreateInfo& VKLDeviceCreateInfo::addExtension(const char* extension) {
	LOG_INFO("Adding extension %s", extension);

	m_extensions.push_back(extension);
	
	m_createInfo.enabledExtensionCount = m_extensions.size();
	m_createInfo.ppEnabledExtensionNames = m_extensions.data();
	
	return invalidate();
}

void VKLDeviceCreateInfo::printSelections() {
	if (!validate()) {
		printf("VKLDeviceCreateInfo not valid\n");
		return;
	}

	_printSelections();
}

bool VKLDeviceCreateInfo::supportsExtension(const char* extension) {
	if (!validate()) {
		printf("VKLDeviceCreateInfo not valid\n");
		return false;
	}

	return _supportsExtension(extension);
}

bool VKLDeviceCreateInfo::supportsLayer(const char* layer) {
	if (!validate()) {
		printf("VKLDeviceCreateInfo not valid\n");
		return false;
	}

	return _supportsLayer(layer);
}

void VKLDeviceCreateInfo::_printSelections() {
	printf("Device Extensions:\n");
	for (uint32_t i = 0; i < m_physicalDevice->getExtensions().size(); ++i) {
		printf("\tExtension ");
		if (i < 10) {
			printf(" ");
		}
		printf(" %d: %s", i, m_physicalDevice->getExtensions()[i].extensionName);
		for (uint32_t j = 0; j < m_extensions.size(); ++j) {
			if (strcmp(m_physicalDevice->getExtensions()[i].extensionName, m_extensions[j]) == 0) {
				for (int k = 0; k < 50 - strlen(m_physicalDevice->getExtensions()[i].extensionName); k++) {
					printf(" ");
				}
				printf(" - Selected");
			}
		}
		printf("\n");
	}	
}

bool VKLDeviceCreateInfo::_supportsExtension(const char* extension) {
	for (int i = 0; i < m_physicalDevice->getExtensions().size(); i++) {
		if (strcmp(m_physicalDevice->getExtensions()[i].extensionName, extension) == 0) {
			LOG_INFO("Extension %s supported", extension);
			return true;
		}
	}

	LOG_INFO("Extension %s unsupported", extension);
	return false;
}

bool VKLDeviceCreateInfo::_supportsLayer(const char* layer) {
	return true;
}

static int32_t getQueueFamilyWithProperties(const VKLPhysicalDevice* physicalDevice, const std::vector<VkQueueFamilyProperties>& queueFamilyProperties,VkQueueFlags supportFlags, VkQueueFlags excludeFlags, VkSurfaceKHR surface) {
	for (int i = 0; i < queueFamilyProperties.size(); i++) {
		if(queueFamilyProperties[i].queueCount == 0) {
			continue;
		}
		
		VkQueueFlags queueFlags = queueFamilyProperties[i].queueFlags;
			
		VkBool32 surfaceSupport = VK_TRUE;
		
		if(surface != VK_NULL_HANDLE) {
			surfaceSupport = physicalDevice->getSurfaceSupport(surface, i);
		}
		
		if ((queueFlags & supportFlags) && !(queueFlags & excludeFlags) && surfaceSupport) {
			return i;
		}
	}

	return -1;
}

static bool allocateQueueType(const VKLPhysicalDevice* physicalDevice, std::vector<VkQueueFamilyProperties>& queueFamilyProperties, uint32_t* queueFamilyCounts,
							  uint32_t typeCount, std::vector<VKLQueueLocation>& typeFamilyIndicies, VkQueueFlags supportedFlags, VkQueueFlags weakExcludeFlags, VkQueueFlags strongExcludeFlags, VkSurfaceKHR surface) {
	VKLQueueLocation tempStackQueueLocation;
	
	for(int i = 0; i < typeCount; i++) {
		int32_t index = getQueueFamilyWithProperties(physicalDevice, queueFamilyProperties, supportedFlags, weakExcludeFlags | strongExcludeFlags, surface);
		
		if(index != -1) {
			tempStackQueueLocation.familyIndex = (uint32_t)index;
			tempStackQueueLocation.localIndex = queueFamilyCounts[index];
			
			typeFamilyIndicies.push_back(tempStackQueueLocation);
			queueFamilyProperties[index].queueCount = queueFamilyProperties[index].queueCount - 1;
			queueFamilyCounts[index] = queueFamilyCounts[index] + 1;
		}
	}
	
	for(int i = typeFamilyIndicies.size(); i < typeCount; i++) {
		int32_t index = getQueueFamilyWithProperties(physicalDevice, queueFamilyProperties, supportedFlags, strongExcludeFlags, surface);
		
		if(index != -1) {
			tempStackQueueLocation.familyIndex = (uint32_t)index;
			tempStackQueueLocation.localIndex = queueFamilyCounts[index];
			typeFamilyIndicies.push_back(tempStackQueueLocation);
			queueFamilyProperties[index].queueCount = queueFamilyProperties[index].queueCount - 1;
			queueFamilyCounts[index] = queueFamilyCounts[index] + 1;
		}
	}
	
	for(int i = typeFamilyIndicies.size(); i < typeCount; i++) {
		int32_t index = getQueueFamilyWithProperties(physicalDevice, queueFamilyProperties, supportedFlags, 0, surface);
		
		if(index != -1) {
			tempStackQueueLocation.familyIndex = (uint32_t)index;
			tempStackQueueLocation.localIndex = queueFamilyCounts[index];
			typeFamilyIndicies.push_back(tempStackQueueLocation);
			queueFamilyProperties[index].queueCount = queueFamilyProperties[index].queueCount - 1;
			queueFamilyCounts[index] = queueFamilyCounts[index] + 1;
		}
	}
	
	return typeFamilyIndicies.size() == typeCount;
}

bool VKLDeviceCreateInfo::_validate() {
#ifdef VKL_VALIDATION
	if(m_physicalDevice == NULL) {
		printf("VKL Validation Error: VKLDeviceCreateInfo::physicalDevice was not set!\n");
		return false;
	}
#endif

#ifdef VKL_VALIDATION
	/*
	for (VkLayerProperties layerProps : supportedLayers) {
		if (!_supportsLayer(layerProps.layerName)) {
			printf("VKL Validation Error: Layer '%s' is not supported by instance!\n", layerProps.layerName);
			return false;
		}
	}
	*/

	for (const char* ext : m_extensions) {
		if (!_supportsExtension(ext)) {
			printf("VKL Validation Error: Extension '%s' is not supported by device!\n", ext);
			return false;
		}
	}
#endif

	if (_supportsExtension("VK_KHR_portability_subset")) {
		addExtension("VK_KHR_portability_subset");
	}

	if(_supportsExtension("VK_KHR_shader_non_semantic_info")) {
		addExtension("VK_KHR_shader_non_semantic_info");
	}

	if(_supportsExtension("VK_EXT_shader_atomic_float")) {
		addExtension("VK_EXT_shader_atomic_float");
	}

	

	//_printSelections();
	
	m_queueCreateInfos.clear();
	m_queueTypeIndicies[0].clear();
	m_queueTypeIndicies[1].clear();
	m_queueTypeIndicies[2].clear();
	m_queueTypeIndicies[3].clear();
	
	std::vector<VkQueueFamilyProperties> queueFamilyProperties = m_physicalDevice->getQueueFamilyProperties();
	
	uint32_t* queueFamilyCounts = (uint32_t*)malloc(sizeof(uint32_t) * queueFamilyProperties.size());
	memset(queueFamilyCounts, 0, sizeof(uint32_t) * queueFamilyProperties.size());
	
	if(!allocateQueueType(m_physicalDevice, queueFamilyProperties, queueFamilyCounts,
							m_queueTypeCounts[VKL_QUEUE_TYPE_ALL], m_queueTypeIndicies[VKL_QUEUE_TYPE_ALL],
							VK_QUEUE_GRAPHICS_BIT | VK_QUEUE_COMPUTE_BIT | VK_QUEUE_TRANSFER_BIT, 0, 0, (VkSurfaceKHR)VK_NULL_HANDLE)) {
		free(queueFamilyCounts);
		
		printf("VKL Validation Error: Could not allocate the requested number of 'all' queues!\n");
		return false;
	}

	if(!allocateQueueType(m_physicalDevice, queueFamilyProperties, queueFamilyCounts,
							m_queueTypeCounts[VKL_QUEUE_TYPE_GRAPHICS], m_queueTypeIndicies[VKL_QUEUE_TYPE_GRAPHICS],
							VK_QUEUE_GRAPHICS_BIT, VK_QUEUE_TRANSFER_BIT, VK_QUEUE_COMPUTE_BIT, (VkSurfaceKHR)VK_NULL_HANDLE)) {
		free(queueFamilyCounts);
		
		printf("VKL Validation Error: Could not allocate the requested number of graphics queues!\n");
		return false;
	}
	
	if(!allocateQueueType(m_physicalDevice, queueFamilyProperties, queueFamilyCounts,
							m_queueTypeCounts[VKL_QUEUE_TYPE_COMPUTE], m_queueTypeIndicies[VKL_QUEUE_TYPE_COMPUTE],
							VK_QUEUE_COMPUTE_BIT, VK_QUEUE_TRANSFER_BIT, VK_QUEUE_GRAPHICS_BIT, (VkSurfaceKHR)VK_NULL_HANDLE)) {
		free(queueFamilyCounts);
		
		printf("VKL Validation Error: Could not allocate the requested number of compute queues!\n");
		return false;
	}
	
	if(!allocateQueueType(m_physicalDevice, queueFamilyProperties, queueFamilyCounts,
							m_queueTypeCounts[VKL_QUEUE_TYPE_TRANSFER], m_queueTypeIndicies[VKL_QUEUE_TYPE_TRANSFER],
							VK_QUEUE_TRANSFER_BIT, VK_QUEUE_COMPUTE_BIT, VK_QUEUE_GRAPHICS_BIT, (VkSurfaceKHR)VK_NULL_HANDLE)) {
		free(queueFamilyCounts);
		
		printf("VKL Validation Error: Could not allocate the requested number of transfer queues!\n");
		return false;
	}
	
	for(int i = 0; i < queueFamilyProperties.size(); i++) {
		if(queueFamilyCounts[i] > 0) {
			float* priorities = (float*)malloc(sizeof(float) * queueFamilyCounts[i]); //TODO: free these allocations in a destructor
			
			for(int j = 0; j < queueFamilyCounts[i]; j++) {
				priorities[j] = 1.0f;
			}
			
			VkDeviceQueueCreateInfo queueCreateInfo;
			queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
			queueCreateInfo.pNext = NULL;
			queueCreateInfo.flags = 0;
			queueCreateInfo.queueFamilyIndex = i;
			queueCreateInfo.queueCount = queueFamilyCounts[i];
			queueCreateInfo.pQueuePriorities = priorities;
			
			m_queueCreateInfos.push_back(queueCreateInfo);
		}
	}
	
	m_createInfo.queueCreateInfoCount = m_queueCreateInfos.size();
	m_createInfo.pQueueCreateInfos = m_queueCreateInfos.data();
	
	free(queueFamilyCounts);
	
	return true;
}
