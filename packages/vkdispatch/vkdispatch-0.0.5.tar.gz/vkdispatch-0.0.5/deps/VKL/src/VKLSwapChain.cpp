#include <VKL/VKL.h>

VKLSwapChain::VKLSwapChain() : VKLCreator<VKLSwapChainCreateInfo>("VKLSwapChain") {
	
}

VKLSwapChain::VKLSwapChain(const VKLSwapChainCreateInfo& createInfo) : VKLCreator<VKLSwapChainCreateInfo>("VKLSwapChain")  {
	this->create(createInfo);
}

void VKLSwapChain::rebuild() {
	VkSurfaceCapabilitiesKHR surfaceCapabilities = m_device->physical()->getSurfaceCapabilities(m_createInfo.m_surface->handle());
	rebuild(surfaceCapabilities.currentExtent.width, surfaceCapabilities.currentExtent.height);
}

void VKLSwapChain::rebuild(uint32_t width, uint32_t height) {
	delete[] m_swapChainImages;
	
	VkExtent2D size;
	size.width = width;
	size.height = height;
	
	m_createInfo.size(size);
	
	VkSwapchainKHR temphandle = m_handle;
	
	rebuild(m_handle);
	
	m_device->vk.DestroySwapchainKHR(m_device->handle(), temphandle, m_device->allocationCallbacks());
}

void VKLSwapChain::rebuild(VkSwapchainKHR oldSwapchain) {
	m_createInfo.m_createInfo.oldSwapchain = oldSwapchain;
	
	VK_CALL(m_device->vk.CreateSwapchainKHR(m_device->handle(), &m_createInfo.m_createInfo, m_device->allocationCallbacks(), &m_handle));

	VkImage* presentImages = NULL;

	m_device->vk.GetSwapchainImagesKHR(m_device->handle(), m_handle, &m_swapChainImageCount, NULL);
	presentImages = (VkImage*)malloc(sizeof(VkImage) * m_swapChainImageCount);
	m_device->vk.GetSwapchainImagesKHR(m_device->handle(), m_handle, &m_swapChainImageCount, presentImages);

	m_swapChainImages = new VKLImage[m_swapChainImageCount];
	
	VKLImageCreateInfo imageCreateInfo;
	imageCreateInfo.device(m_device)
					.format(m_createInfo.m_createInfo.imageFormat)
					.usage(m_createInfo.m_createInfo.imageUsage)
					.extent(m_createInfo.m_createInfo.imageExtent.width, m_createInfo.m_createInfo.imageExtent.height, 1).validate();
	
	m_cmdBuffer->begin();
	
	for(int i = 0; i < m_swapChainImageCount; i++) {
		m_swapChainImages[i]._create(imageCreateInfo, presentImages[i]);
		m_swapChainImages[i].cmdTransitionBarrier(m_cmdBuffer, VK_ACCESS_TRANSFER_WRITE_BIT, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT);
	}

	free(presentImages);
	
	m_cmdBuffer->end();
	
	m_queue->submit(m_cmdBuffer);
	m_queue->waitIdle();
	
	VK_CALL(m_device->vk.AcquireNextImageKHR(m_device->handle(), m_handle, UINT64_MAX, (VkSemaphore)VK_NULL_HANDLE, m_fence, &m_currentImgIndex));
	
	m_device->waitForFence(m_fence);
	m_device->resetFence(m_fence);
}

void VKLSwapChain::_create(const VKLSwapChainCreateInfo& createInfo) {
	m_createInfo = createInfo;
	m_device = m_createInfo.m_queue->device();
	m_queue = m_createInfo.m_queue;
	m_cmdBuffer = new VKLCommandBuffer(m_queue);
	m_fence = m_device->createFence(0);
	
	rebuild((VkSwapchainKHR)VK_NULL_HANDLE);
}

VKLImage& VKLSwapChain::getCurrentImage() {
	return m_swapChainImages[m_currentImgIndex];
}

void VKLSwapChain::present(const VKLImage* image) {
	present(image, 0, NULL, NULL);
}

void VKLSwapChain::present(const VKLImage* image, uint32_t waitSemaphoreCount, const VkSemaphore* waitSemaphores, const VkPipelineStageFlags* pWaitDstStageMask) {
	VkImageBlit imageBlit;
	memset(&imageBlit, 0, sizeof(VkImageBlit));
	imageBlit.srcSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
	imageBlit.srcSubresource.layerCount = 1;
	imageBlit.srcOffsets[1].x = image->extent().width;
	imageBlit.srcOffsets[1].y = image->extent().height;
	imageBlit.srcOffsets[1].z = 1;
	imageBlit.dstSubresource = imageBlit.srcSubresource;
	imageBlit.dstOffsets[1].x = getCurrentImage().extent().width;
	imageBlit.dstOffsets[1].y = getCurrentImage().extent().height;
	imageBlit.dstOffsets[1].z = 1;
	
	//printf("(%d, %d) (%d, %d)\n", imageBlit.srcOffsets[1].x, imageBlit.srcOffsets[1].y, imageBlit.dstOffsets[1].x, imageBlit.dstOffsets[1].y);
	
	m_cmdBuffer->begin();
	
	m_device->vk.CmdBlitImage(m_cmdBuffer->handle(), image->handle(), image->layout(), getCurrentImage().handle(), VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, 1, &imageBlit, VK_FILTER_LINEAR);
	
	getCurrentImage().cmdTransitionBarrier(m_cmdBuffer, VK_ACCESS_MEMORY_READ_BIT, VK_IMAGE_LAYOUT_PRESENT_SRC_KHR, VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT);
	m_cmdBuffer->end();
	
	m_queue->submit(m_cmdBuffer, NULL, waitSemaphoreCount, waitSemaphores, pWaitDstStageMask);
	m_queue->waitIdle();
	
	VkPresentInfoKHR presentInfo;
	presentInfo.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
	presentInfo.pNext = NULL;
	presentInfo.waitSemaphoreCount = 0;
	presentInfo.pWaitSemaphores = NULL;
	presentInfo.swapchainCount = 1;
	presentInfo.pSwapchains = &m_handle;
	presentInfo.pImageIndices = &m_currentImgIndex;
	presentInfo.pResults = NULL;
	
	VK_CALL(m_device->vk.QueuePresentKHR(m_queue->handle(), &presentInfo));
	
	m_cmdBuffer->begin();
	getCurrentImage().cmdTransitionBarrier(m_cmdBuffer, VK_ACCESS_TRANSFER_WRITE_BIT, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT);
	m_cmdBuffer->end();
	
	m_queue->submit(m_cmdBuffer);
	m_queue->waitIdle();
	
	VK_CALL(m_device->vk.AcquireNextImageKHR(m_device->handle(), m_handle, UINT64_MAX, (VkSemaphore)VK_NULL_HANDLE, m_fence, &m_currentImgIndex));
	
	m_device->waitForFence(m_fence);
	m_device->resetFence(m_fence);
}

void VKLSwapChain::_destroy() {
	m_device->destroyFence(m_fence);
	
	delete[] m_swapChainImages;
	
	m_cmdBuffer->destroy();
	
	delete m_cmdBuffer;

	m_device->vk.DestroySwapchainKHR(m_device->handle(), m_handle, m_device->allocationCallbacks());
}

VKLSwapChainCreateInfo::VKLSwapChainCreateInfo() {
	m_queue = NULL;
	
	memset(&m_createInfo, 0, sizeof(VkSwapchainCreateInfoKHR));
	m_createInfo.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
	m_createInfo.pNext = NULL;
	m_createInfo.flags = 0;
	m_createInfo.surface = (VkSurfaceKHR)VK_NULL_HANDLE;
	m_createInfo.minImageCount = 2;
	m_createInfo.imageFormat = VK_FORMAT_UNDEFINED;
	m_createInfo.imageExtent.width = -1;
	m_createInfo.imageExtent.height = -1;
	m_createInfo.imageArrayLayers = 1;
	m_createInfo.imageUsage = VK_IMAGE_USAGE_TRANSFER_DST_BIT;
	m_createInfo.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
	m_createInfo.queueFamilyIndexCount = 0;
	m_createInfo.pQueueFamilyIndices = NULL;
	m_createInfo.preTransform = VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR;
	m_createInfo.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
	m_createInfo.presentMode = VK_PRESENT_MODE_FIFO_KHR;
	m_createInfo.clipped = VK_TRUE;
	m_createInfo.oldSwapchain = (VkSwapchainKHR)VK_NULL_HANDLE;
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::queue(const VKLQueue* queue) {
	m_queue = queue;
	
	return invalidate();
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::surface(const VKLSurface* surface) {
	m_surface = surface;
	m_createInfo.surface = m_surface->handle();
	
	return invalidate();
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::size(VkExtent2D size) {
	m_createInfo.imageExtent = size;
	
	return invalidate();
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::imageFormat(VkFormat format) {
	m_createInfo.imageFormat = format;
	
	return invalidate();
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::imageCount(uint32_t imageCount) {
	m_createInfo.minImageCount = imageCount;
	
	return invalidate();
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::preTransform(VkSurfaceTransformFlagBitsKHR preTransform) {
	m_createInfo.preTransform = preTransform;
	
	return invalidate();
}

VKLSwapChainCreateInfo& VKLSwapChainCreateInfo::presentMode(VkPresentModeKHR presentMode) {
	m_createInfo.presentMode = presentMode;
	
	return invalidate();
}

bool VKLSwapChainCreateInfo::_validate() {
	if(m_queue == NULL) {
		printf("VKL Validation Error: VKLSwapChainCreateInfo::queue was not set!\n");
		return false;
	}

	if (m_createInfo.surface == VK_NULL_HANDLE) {
		printf("VKL Validation Error: VKLSwapChainCreateInfo::surface was not set!\n");
		return false;
	}
	
	const VKLPhysicalDevice* physicalDevice = m_queue->device()->physical();
	
	if(!physicalDevice->getSurfaceSupport(m_createInfo.surface, m_queue->getFamilyIndex())) {
		return false;
	}
	
	std::vector<VkSurfaceFormatKHR> surfaceFormats = physicalDevice->getSurfaceFormats(m_createInfo.surface);
	
	VkBool32 foundFormat = VK_FALSE;
	
	for(VkSurfaceFormatKHR surfaceFormat : surfaceFormats) {
		if(surfaceFormat.format == m_createInfo.imageFormat) {
			m_createInfo.imageColorSpace = surfaceFormat.colorSpace;
			foundFormat = VK_TRUE;
		}
	}
	
	if(!foundFormat) {
		if (m_createInfo.imageFormat != VK_FORMAT_UNDEFINED) {
			printf("VKL Validation Warning: Requested format is not supported by the surface!\n");
			printf("                        Reverting to first supported format from vkGetPhysicalDeviceSurfaceFormatsKHR (VkFormat = %d)\n", surfaceFormats[0].format);
		}

		m_createInfo.imageFormat = surfaceFormats[0].format;
		m_createInfo.imageColorSpace = surfaceFormats[0].colorSpace;
	}
	
	VkSurfaceCapabilitiesKHR surfaceCapabilities = physicalDevice->getSurfaceCapabilities(m_createInfo.surface);

	if (m_createInfo.minImageCount < surfaceCapabilities.minImageCount) {
		m_createInfo.minImageCount = surfaceCapabilities.minImageCount;
	}
	else if (surfaceCapabilities.maxImageCount != 0 && m_createInfo.minImageCount > surfaceCapabilities.maxImageCount) {
		m_createInfo.minImageCount = surfaceCapabilities.maxImageCount;
	}
	
	if(surfaceCapabilities.currentExtent.width == -1) {
		if(m_createInfo.imageExtent.width == -1) {
			m_createInfo.imageExtent.width = 800;
		}
		
		if(m_createInfo.imageExtent.width < surfaceCapabilities.minImageExtent.width) {
			m_createInfo.imageExtent.width = surfaceCapabilities.minImageExtent.width;
		}
		
		if(m_createInfo.imageExtent.width > surfaceCapabilities.maxImageExtent.width) {
			m_createInfo.imageExtent.width = surfaceCapabilities.maxImageExtent.width;
		}
	} else {
		m_createInfo.imageExtent.width = surfaceCapabilities.currentExtent.width;
	}
	
	if(surfaceCapabilities.currentExtent.height == -1) {
		if(m_createInfo.imageExtent.height == -1) {
			m_createInfo.imageExtent.height = 600;
		}
		
		if(m_createInfo.imageExtent.height < surfaceCapabilities.minImageExtent.height) {
			m_createInfo.imageExtent.height = surfaceCapabilities.minImageExtent.height;
		}
		
		if(m_createInfo.imageExtent.height > surfaceCapabilities.maxImageExtent.height) {
			m_createInfo.imageExtent.height = surfaceCapabilities.maxImageExtent.height;
		}
	} else {
		m_createInfo.imageExtent.height = surfaceCapabilities.currentExtent.height;
	}
	
	//TODO: finish checking for support of parameters specified by surfaceCapabilities
	
	std::vector<VkPresentModeKHR> presentModes = physicalDevice->getSurfacePresentModes(m_createInfo.surface);
	
	VkBool32 foundPresentMode = VK_FALSE;
	
	for(VkPresentModeKHR presentMode : presentModes) {
		if(presentMode == m_createInfo.presentMode) {
			foundPresentMode = VK_TRUE;
		}
	}
	
	if(!foundPresentMode) {
		m_createInfo.presentMode = VK_PRESENT_MODE_FIFO_KHR;
	}
	
	return true;
}
