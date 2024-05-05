#include <VKL/VKL.h>

VKLPhysicalDevice::VKLPhysicalDevice(VkPhysicalDevice physicalDevice, const VKLInstance* instance) {
	m_handle = physicalDevice;
	m_instance = instance;

	m_features.sType = VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2;
	m_features.pNext = &m_atomicFloatFeatures;

	m_atomicFloatFeatures = {};
	m_atomicFloatFeatures.sType = VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_SHADER_ATOMIC_FLOAT_FEATURES_EXT;
	m_atomicFloatFeatures.pNext = NULL;

	m_properties.sType = VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2;
	m_properties.pNext = &m_subgroupProperties;

	m_subgroupProperties = {};
	m_subgroupProperties.sType = VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_SUBGROUP_PROPERTIES;
	m_subgroupProperties.pNext = NULL;

	vkGetPhysicalDeviceFeatures2(m_handle, &m_features);
	vkGetPhysicalDeviceProperties2(m_handle, &m_properties);
	
	vkGetPhysicalDeviceMemoryProperties(m_handle, &m_memoryProperties);

	VkQueueFamilyProperties* queueFamilyProperties = NULL;
	uint32_t queueFamilyPropertyCount = 0;

	vkGetPhysicalDeviceQueueFamilyProperties(m_handle, &queueFamilyPropertyCount, NULL);
	queueFamilyProperties = (VkQueueFamilyProperties*)malloc(sizeof(VkQueueFamilyProperties) * queueFamilyPropertyCount);
	vkGetPhysicalDeviceQueueFamilyProperties(m_handle, &queueFamilyPropertyCount, queueFamilyProperties);

	for (int i = 0; i < queueFamilyPropertyCount; i++) {
		m_queueFamilyProperties.push_back(queueFamilyProperties[i]);
	}

	free(queueFamilyProperties);
	
	uint32_t extensionCount = 0;
	vkEnumerateDeviceExtensionProperties(m_handle, NULL, &extensionCount, NULL);
	m_extensions.resize(extensionCount);
	vkEnumerateDeviceExtensionProperties(m_handle, NULL, &extensionCount, m_extensions.data());
}

const VKLInstance* VKLPhysicalDevice::instance() const {
	return m_instance;
}

VkPhysicalDeviceFeatures2 VKLPhysicalDevice::getFeatures2() const {
	return m_features;
}

VkPhysicalDeviceFeatures VKLPhysicalDevice::getFeatures() const {
	return m_features.features;
}

VkPhysicalDeviceShaderAtomicFloatFeaturesEXT VKLPhysicalDevice::getAtomicFloatFeatures() const {
	return m_atomicFloatFeatures;
}

VkFormatProperties VKLPhysicalDevice::getFormatProperties(VkFormat format) const {
	VkFormatProperties result;
	vkGetPhysicalDeviceFormatProperties(m_handle, format, &result);
	return result;
}

VkImageFormatProperties VKLPhysicalDevice::getImageFormatProperties(VkFormat format, VkImageType type, VkImageTiling tiling, VkImageUsageFlags usage, VkImageCreateFlags flags) const {
	VkImageFormatProperties result;
	VK_CALL(vkGetPhysicalDeviceImageFormatProperties(m_handle, format, type, tiling, usage, flags, &result));
	return result;
}

VkPhysicalDeviceProperties VKLPhysicalDevice::getProperties() const {
	return m_properties.properties;
}

VkPhysicalDeviceProperties2 VKLPhysicalDevice::getProperties2() const {
	return m_properties;
}

VkPhysicalDeviceSubgroupProperties VKLPhysicalDevice::getSubgroupProperties() const {
	return m_subgroupProperties;
}

const std::vector<VkQueueFamilyProperties>& VKLPhysicalDevice::getQueueFamilyProperties() const {
	return m_queueFamilyProperties;
}

VkPhysicalDeviceMemoryProperties VKLPhysicalDevice::getMemoryProperties() const {
	return m_memoryProperties;
}

const std::vector<VkExtensionProperties>& VKLPhysicalDevice::getExtensions() const {
	return m_extensions;
}

VkBool32 VKLPhysicalDevice::getSurfaceSupport(VkSurfaceKHR surface, uint32_t queueFamilyIndex) const {
	VkBool32 result = VK_FALSE;
	VK_CALL(vkGetPhysicalDeviceSurfaceSupportKHR(m_handle, queueFamilyIndex, surface, &result));
	return result;
}

VkSurfaceCapabilitiesKHR VKLPhysicalDevice::getSurfaceCapabilities(VkSurfaceKHR surface) const {
	VkSurfaceCapabilitiesKHR result;
	vkGetPhysicalDeviceSurfaceCapabilitiesKHR(m_handle, surface, &result);
	return result;
}

std::vector<VkSurfaceFormatKHR> VKLPhysicalDevice::getSurfaceFormats(VkSurfaceKHR surface) const {
	std::vector<VkSurfaceFormatKHR> result;
	uint32_t count;
	vkGetPhysicalDeviceSurfaceFormatsKHR(m_handle, surface, &count, NULL);
	result.resize(count);
	vkGetPhysicalDeviceSurfaceFormatsKHR(m_handle, surface, &count, result.data());
	return result;
}

std::vector<VkPresentModeKHR> VKLPhysicalDevice::getSurfacePresentModes(VkSurfaceKHR surface) const {
	std::vector<VkPresentModeKHR> result;
	uint32_t count;
	vkGetPhysicalDeviceSurfacePresentModesKHR(m_handle, surface, &count, NULL);
	result.resize(count);
	vkGetPhysicalDeviceSurfacePresentModesKHR(m_handle, surface, &count, result.data());
	return result;
}
