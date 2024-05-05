#ifndef VKLPhysicalDevice_h
#define VKLPhysicalDevice_h

#include "VKL_base.h"

#include <vector>

class VKLPhysicalDevice : public VKLHandle<VkPhysicalDevice> {
public:
	const VKLInstance* instance() const;

	VkPhysicalDeviceFeatures getFeatures() const;
	VkPhysicalDeviceFeatures2 getFeatures2() const;
	VkPhysicalDeviceShaderAtomicFloatFeaturesEXT getAtomicFloatFeatures() const;	
	VkFormatProperties getFormatProperties(VkFormat format) const;
	VkImageFormatProperties getImageFormatProperties(VkFormat format, VkImageType type, VkImageTiling tiling, VkImageUsageFlags usage, VkImageCreateFlags flags) const;
	VkPhysicalDeviceProperties getProperties() const;
	VkPhysicalDeviceProperties2 getProperties2() const;
	VkPhysicalDeviceSubgroupProperties getSubgroupProperties() const;
	const std::vector<VkQueueFamilyProperties>& getQueueFamilyProperties() const;
	VkPhysicalDeviceMemoryProperties getMemoryProperties() const;
	const std::vector<VkExtensionProperties>& getExtensions() const;
	
	VkBool32 getSurfaceSupport(VkSurfaceKHR surface, uint32_t queueFamilyIndex) const;
	VkSurfaceCapabilitiesKHR getSurfaceCapabilities(VkSurfaceKHR surface) const;
	std::vector<VkSurfaceFormatKHR> getSurfaceFormats(VkSurfaceKHR surface) const;
	std::vector<VkPresentModeKHR> getSurfacePresentModes(VkSurfaceKHR surface) const;
private:
	VKLPhysicalDevice(VkPhysicalDevice physicalDevice, const VKLInstance* instance);

	const VKLInstance* m_instance;

	VkPhysicalDeviceFeatures2 m_features;
	VkPhysicalDeviceShaderAtomicFloatFeaturesEXT m_atomicFloatFeatures;
	VkPhysicalDeviceProperties2 m_properties;
	VkPhysicalDeviceSubgroupProperties m_subgroupProperties;
	std::vector<VkQueueFamilyProperties> m_queueFamilyProperties;
	std::vector<VkExtensionProperties> m_extensions;
	VkPhysicalDeviceMemoryProperties m_memoryProperties;

	friend class VKLInstance;
};

#endif
