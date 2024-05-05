#include <VKL/VKL.h>

VKLImageView::VKLImageView() : VKLCreator<VKLImageViewCreateInfo>("VKLImageView") {
	m_device = NULL;
	m_image = NULL;
}

VKLImageView::VKLImageView(const VKLImageViewCreateInfo& createInfo) : VKLCreator<VKLImageViewCreateInfo>("VKLImageView") {
	m_device = NULL;
	m_image = NULL;
	create(createInfo);
}

const VKLImage* VKLImageView::image() const {
	return m_image;
}

void VKLImageView::_destroy() {
	m_device->vk.DestroyImageView(m_device->handle(), m_handle, m_device->allocationCallbacks());
}

void VKLImageView::_create(const VKLImageViewCreateInfo& createInfo) {
	m_image = createInfo.m_image;
	m_device = m_image->m_device;

	VK_CALL(m_device->vk.CreateImageView(m_device->handle(), &createInfo.m_createInfo, m_device->allocationCallbacks(), &m_handle));
}

VKLImageViewCreateInfo::VKLImageViewCreateInfo() {
	memset(&m_createInfo, 0, sizeof(VkImageViewCreateInfo));
	m_createInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
	m_createInfo.pNext = NULL;
	m_createInfo.flags = 0;
	m_createInfo.image = (VkImage)VK_NULL_HANDLE;
	m_createInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
	m_createInfo.format = VK_FORMAT_UNDEFINED;
	m_createInfo.components.r = VK_COMPONENT_SWIZZLE_IDENTITY;
	m_createInfo.components.g = VK_COMPONENT_SWIZZLE_IDENTITY;
	m_createInfo.components.b = VK_COMPONENT_SWIZZLE_IDENTITY;
	m_createInfo.components.a = VK_COMPONENT_SWIZZLE_IDENTITY;
	m_createInfo.subresourceRange.baseMipLevel = 0;
	m_createInfo.subresourceRange.levelCount = 1;
	m_createInfo.subresourceRange.baseArrayLayer = 0;
	m_createInfo.subresourceRange.layerCount = 1;
}

VKLImageViewCreateInfo& VKLImageViewCreateInfo::image(const VKLImage* image) {
	m_image = image;

	m_createInfo.image = m_image->handle();

	return invalidate();
}

VKLImageViewCreateInfo& VKLImageViewCreateInfo::type(VkImageViewType type) {
	m_createInfo.viewType = type;

	return invalidate();
}

VKLImageViewCreateInfo& VKLImageViewCreateInfo::format(VkFormat format) {
	m_createInfo.format = format;

	return invalidate();
}

bool VKLImageViewCreateInfo::_validate() {
	if (m_image == NULL) {
		printf("VKL Validation Error: VKLImageViewCreateInfo::image is not set!\n");
		return false;
	}

	if (m_createInfo.format == VK_FORMAT_UNDEFINED) {
		m_createInfo.format = m_image->format();
	}
	
	
	m_createInfo.subresourceRange.aspectMask = m_image->aspect();
	m_createInfo.subresourceRange.layerCount = m_image->layers();
	
	return true;
}
