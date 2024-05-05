#ifndef VKLInstance_h
#define VKLInstance_h

#include <VKL/VKL_base.h>
#include <VKL/VKLPhysicalDevice.h>

#include <vector>

/*

typedef struct VKLInstancePFNS {
	PFN_vkCreateInstance CreateInstance;
	PFN_vkDestroyInstance DestroyInstance;
	PFN_vkEnumeratePhysicalDevices EnumeratePhysicalDevices;
	PFN_vkGetInstanceProcAddr GetInstanceProcAddr;
	PFN_vkEnumerateInstanceExtensionProperties EnumerateInstanceExtensionProperties;
	PFN_vkEnumerateInstanceLayerProperties EnumerateInstanceLayerProperties;

	PFN_vkCreateDebugUtilsMessengerEXT CreateDebugUtilsMessengerEXT;
	PFN_vkDestroyDebugUtilsMessengerEXT DestroyDebugUtilsMessengerEXT;

	PFN_vkGetPhysicalDeviceFeatures GetPhysicalDeviceFeatures;
	PFN_vkGetPhysicalDeviceFormatProperties GetPhysicalDeviceFormatProperties;
	PFN_vkGetPhysicalDeviceImageFormatProperties GetPhysicalDeviceImageFormatProperties;
	PFN_vkGetPhysicalDeviceProperties GetPhysicalDeviceProperties;
	PFN_vkGetPhysicalDeviceProperties2 GetPhysicalDeviceProperties2;
	PFN_vkGetPhysicalDeviceQueueFamilyProperties GetPhysicalDeviceQueueFamilyProperties;
	PFN_vkGetPhysicalDeviceMemoryProperties GetPhysicalDeviceMemoryProperties;
	PFN_vkGetPhysicalDeviceSparseImageFormatProperties GetPhysicalDeviceSparseImageFormatProperties;

	PFN_vkCreateDevice CreateDevice;
	PFN_vkDestroyDevice DestroyDevice;
	PFN_vkEnumerateDeviceExtensionProperties EnumerateDeviceExtensionProperties;
	PFN_vkEnumerateDeviceLayerProperties EnumerateDeviceLayerProperties;

	PFN_vkDestroySurfaceKHR DestroySurfaceKHR;
	PFN_vkGetPhysicalDeviceSurfaceSupportKHR GetPhysicalDeviceSurfaceSupportKHR;
	PFN_vkGetPhysicalDeviceSurfaceCapabilitiesKHR GetPhysicalDeviceSurfaceCapabilitiesKHR;
	PFN_vkGetPhysicalDeviceSurfaceFormatsKHR GetPhysicalDeviceSurfaceFormatsKHR;
	PFN_vkGetPhysicalDeviceSurfacePresentModesKHR GetPhysicalDeviceSurfacePresentModesKHR;

#ifdef VKL_SURFACE_WIN32
	PFN_vkVoidFunction CreateWin32SurfaceKHR;
	PFN_vkVoidFunction GetPhysicalDeviceWin32PresentationSupportKHR;
#endif
	
#ifdef VKL_SURFACE_MACOS
	PFN_vkVoidFunction CreateMetalSurfaceEXT;
#endif
} __VKLInstancePFNS;
*/

class VKLInstanceCreateInfo : public VKLCreateInfo<VKLInstanceCreateInfo>{
public:
	VKLInstanceCreateInfo();
	
	VKLInstanceCreateInfo& allocationCallbacks(VkAllocationCallbacks* allocationCallbacks);
	VKLInstanceCreateInfo& addLayer(const char* layer);
	VKLInstanceCreateInfo& addExtension(const char* extension);
	VKLInstanceCreateInfo& addExtensions(const char** extensions, uint32_t extensionCount);
	VKLInstanceCreateInfo& debug(VkBool32 debug);
	
	void printSelections();
	
	bool supportsExtension(const char* extension);
	bool supportsLayer(const char* layer);
	
	std::vector<VkExtensionProperties> supportedExtensions;
	std::vector<VkLayerProperties> supportedLayers;
private:
	PFN_vkEnumerateInstanceExtensionProperties m_vkEnumerateInstanceExtensionProperties;
	PFN_vkEnumerateInstanceLayerProperties m_vkEnumerateInstanceLayerProperties;

	VkApplicationInfo m_appInfo;
	VkInstanceCreateInfo m_createInfo;

	VkAllocationCallbacks* m_allocationCallbacks;

	void _printSelections();

	bool _supportsExtension(const char* extension);
	bool _supportsLayer(const char* layer);

	std::vector<const char*> m_layers;
	std::vector<const char*> m_extensions;

	VkBool32 m_debug;

	bool _validate();

	friend class VKLInstance;
};

class VKLInstance : public VKLHandle<VkInstance>, public VKLCreator<VKLInstanceCreateInfo> {
public:
	VKLInstance();
	VKLInstance(const VKLInstanceCreateInfo& createInfo);
	
	const VkAllocationCallbacks* allocationCallbacks() const;
	PFN_vkVoidFunction procAddr(const char* name) const;
	const std::vector<VKLPhysicalDevice*>& getPhysicalDevices() const;
	const std::vector<const char*>& getLayers() const;
	const std::vector<const char*>& getExtensions() const;
	
	//VKLInstancePFNS vk;
private:
	const VkAllocationCallbacks* m_allocationCallbacks;

	VkDebugUtilsMessengerEXT debug_messenger;

	VkDebugReportCallbackEXT m_debugCallback;

	std::vector<VKLPhysicalDevice*> m_physicalDevices;
	
	std::vector<const char*> m_layers;
	std::vector<const char*> m_extensions;

	void _create(const VKLInstanceCreateInfo& createInfo);
	void _destroy();
};

#endif
