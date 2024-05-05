#include <VKL/VKL.h>

VKLInstance::VKLInstance() : VKLCreator<VKLInstanceCreateInfo>("VKLInstance") {
	m_handle = (VkInstance)VK_NULL_HANDLE;
	m_allocationCallbacks = NULL;
	m_debugCallback = NULL;
	//memset(&vk, 0, sizeof(VKLInstancePFNS));
}

VKLInstance::VKLInstance(const VKLInstanceCreateInfo& createInfo) : VKLCreator<VKLInstanceCreateInfo>("VKLInstance") {
	m_handle = (VkInstance)VK_NULL_HANDLE;
	m_allocationCallbacks = NULL;
	m_debugCallback = NULL;
	//memset(&vk, 0, sizeof(VKLInstancePFNS));
	this->create(createInfo);
}

VkBool32 VKAPI_PTR mystdOutLogger(
	VkDebugUtilsMessageSeverityFlagBitsEXT           messageSeverity,
	VkDebugUtilsMessageTypeFlagsEXT                  messageTypes,
	const VkDebugUtilsMessengerCallbackDataEXT*      pCallbackData,
	void*                                            pUserData) {
	printf("VKL: %s\n", pCallbackData->pMessage);
	return VK_FALSE;
}

void VKLInstance::_create(const VKLInstanceCreateInfo& createInfo) {
	m_extensions.insert(m_extensions.end(), createInfo.m_extensions.begin(), createInfo.m_extensions.end());
	m_layers.insert(m_layers.end(), createInfo.m_layers.begin(), createInfo.m_layers.end());

	VkValidationFeaturesEXT validationFeatures = {};
	validationFeatures.sType = VK_STRUCTURE_TYPE_VALIDATION_FEATURES_EXT;
	validationFeatures.enabledValidationFeatureCount = 1;

	VkValidationFeatureEnableEXT enabledValidationFeatures[] = {VK_VALIDATION_FEATURE_ENABLE_DEBUG_PRINTF_EXT};
	validationFeatures.pEnabledValidationFeatures = enabledValidationFeatures;

	((VkInstanceCreateInfo*)&createInfo.m_createInfo)->pNext = &validationFeatures;

	VK_CALL(vkCreateInstance(&createInfo.m_createInfo, m_allocationCallbacks, &m_handle));

	volkLoadInstance(m_handle);

	VkDebugUtilsMessengerCreateInfoEXT debugCreateInfo = {};
	debugCreateInfo.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
	debugCreateInfo.pNext = NULL;
    debugCreateInfo.flags = 0;
    debugCreateInfo.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT |
						VK_DEBUG_UTILS_MESSAGE_SEVERITY_INFO_BIT_EXT |
					   VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
					   VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
    debugCreateInfo.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
                       VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT;
    debugCreateInfo.pfnUserCallback = mystdOutLogger;
    debugCreateInfo.pUserData = NULL;

	VK_CALL(vkCreateDebugUtilsMessengerEXT(m_handle, &debugCreateInfo, m_allocationCallbacks, &debug_messenger));	

	VkPhysicalDevice* physicalDevices = NULL;
	uint32_t physicalDeviceCount = 0;

	VK_CALL(vkEnumeratePhysicalDevices(m_handle, &physicalDeviceCount, NULL));
	physicalDevices = (VkPhysicalDevice*)malloc(sizeof(VkPhysicalDevice*) * physicalDeviceCount);
	VK_CALL(vkEnumeratePhysicalDevices(m_handle, &physicalDeviceCount, physicalDevices));

	for (int i = 0; i < physicalDeviceCount; i++) {
		m_physicalDevices.push_back(new VKLPhysicalDevice(physicalDevices[i], this));
	}

	free(physicalDevices);

	/*	
	vk.GetInstanceProcAddr = createInfo.m_procAddr;
	
	vk.CreateInstance = (PFN_vkCreateInstance)procAddr("vkCreateInstance");
	vk.EnumerateInstanceLayerProperties = (PFN_vkEnumerateInstanceLayerProperties)procAddr("vkEnumerateInstanceLayerProperties");
	vk.EnumerateInstanceExtensionProperties = (PFN_vkEnumerateInstanceExtensionProperties)procAddr("vkEnumerateInstanceExtensionProperties");

	m_extensions.insert(m_extensions.end(), createInfo.m_extensions.begin(), createInfo.m_extensions.end());
	m_layers.insert(m_layers.end(), createInfo.m_layers.begin(), createInfo.m_layers.end());

	VkValidationFeaturesEXT validationFeatures = {};
	validationFeatures.sType = VK_STRUCTURE_TYPE_VALIDATION_FEATURES_EXT;
	validationFeatures.enabledValidationFeatureCount = 1;

	VkValidationFeatureEnableEXT enabledValidationFeatures[] = {VK_VALIDATION_FEATURE_ENABLE_DEBUG_PRINTF_EXT};
	validationFeatures.pEnabledValidationFeatures = enabledValidationFeatures;

	((VkInstanceCreateInfo*)&createInfo.m_createInfo)->pNext = &validationFeatures;

	VK_CALL(vkCreateInstance(&createInfo.m_createInfo, m_allocationCallbacks, &m_handle));

	vk.DestroyInstance = (PFN_vkDestroyInstance)procAddr("vkDestroyInstance");
	vk.EnumeratePhysicalDevices = (PFN_vkEnumeratePhysicalDevices)procAddr("vkEnumeratePhysicalDevices");

	vk.CreateDebugUtilsMessengerEXT = (PFN_vkCreateDebugUtilsMessengerEXT)procAddr("vkCreateDebugUtilsMessengerEXT");
	vk.DestroyDebugUtilsMessengerEXT = (PFN_vkDestroyDebugUtilsMessengerEXT)procAddr("vkDestroyDebugUtilsMessengerEXT");

	VkDebugUtilsMessengerCreateInfoEXT debugCreateInfo = {};
	debugCreateInfo.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
	debugCreateInfo.pNext = NULL;
    debugCreateInfo.flags = 0;
    debugCreateInfo.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT |
						VK_DEBUG_UTILS_MESSAGE_SEVERITY_INFO_BIT_EXT |
					   VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
					   VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
    debugCreateInfo.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
                       VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT;
    debugCreateInfo.pfnUserCallback = mystdOutLogger;
    debugCreateInfo.pUserData = NULL;

	VK_CALL(vk.CreateDebugUtilsMessengerEXT(m_handle, &debugCreateInfo, m_allocationCallbacks, &debug_messenger));	

	vk.GetPhysicalDeviceFeatures = (PFN_vkGetPhysicalDeviceFeatures)procAddr("vkGetPhysicalDeviceFeatures");
	vk.GetPhysicalDeviceFormatProperties = (PFN_vkGetPhysicalDeviceFormatProperties)procAddr("vkGetPhysicalDeviceFormatProperties");
	vk.GetPhysicalDeviceImageFormatProperties = (PFN_vkGetPhysicalDeviceImageFormatProperties)procAddr("vkGetPhysicalDeviceImageFormatProperties");
	vk.GetPhysicalDeviceProperties = (PFN_vkGetPhysicalDeviceProperties)procAddr("vkGetPhysicalDeviceProperties");
	vk.GetPhysicalDeviceProperties2 = (PFN_vkGetPhysicalDeviceProperties2)procAddr("vkGetPhysicalDeviceProperties2");
	vk.GetPhysicalDeviceQueueFamilyProperties = (PFN_vkGetPhysicalDeviceQueueFamilyProperties)procAddr("vkGetPhysicalDeviceQueueFamilyProperties");
	vk.GetPhysicalDeviceMemoryProperties = (PFN_vkGetPhysicalDeviceMemoryProperties)procAddr("vkGetPhysicalDeviceMemoryProperties");
	vk.GetPhysicalDeviceSparseImageFormatProperties = (PFN_vkGetPhysicalDeviceSparseImageFormatProperties)procAddr("vkGetPhysicalDeviceSparseImageFormatProperties");

	vk.CreateDevice = (PFN_vkCreateDevice)procAddr("vkCreateDevice");
	vk.DestroyDevice = (PFN_vkDestroyDevice)procAddr("vkDestroyDevice");
	vk.EnumerateDeviceExtensionProperties = (PFN_vkEnumerateDeviceExtensionProperties)procAddr("vkEnumerateDeviceExtensionProperties");
	vk.EnumerateDeviceLayerProperties = (PFN_vkEnumerateDeviceLayerProperties)procAddr("vkEnumerateDeviceLayerProperties");
	
	vk.DestroySurfaceKHR = (PFN_vkDestroySurfaceKHR)procAddr("vkDestroySurfaceKHR");
	vk.GetPhysicalDeviceSurfaceSupportKHR = (PFN_vkGetPhysicalDeviceSurfaceSupportKHR)procAddr("vkGetPhysicalDeviceSurfaceSupportKHR");
	vk.GetPhysicalDeviceSurfaceCapabilitiesKHR = (PFN_vkGetPhysicalDeviceSurfaceCapabilitiesKHR)procAddr("vkGetPhysicalDeviceSurfaceCapabilitiesKHR");
	vk.GetPhysicalDeviceSurfaceFormatsKHR = (PFN_vkGetPhysicalDeviceSurfaceFormatsKHR)procAddr("vkGetPhysicalDeviceSurfaceFormatsKHR");
	vk.GetPhysicalDeviceSurfacePresentModesKHR = (PFN_vkGetPhysicalDeviceSurfacePresentModesKHR)procAddr("vkGetPhysicalDeviceSurfacePresentModesKHR");

#ifdef VKL_SURFACE_WIN32
	vk.CreateWin32SurfaceKHR = procAddr("vkCreateWin32SurfaceKHR");
	vk.GetPhysicalDeviceWin32PresentationSupportKHR = procAddr("vkGetPhysicalDeviceWin32PresentationSupportKHR");
#endif
	
#ifdef VKL_SURFACE_MACOS
	vk.CreateMetalSurfaceEXT = procAddr("vkCreateMetalSurfaceEXT");
#endif


	VkPhysicalDevice* physicalDevices = NULL;
	uint32_t physicalDeviceCount = 0;

	VK_CALL(vk.EnumeratePhysicalDevices(m_handle, &physicalDeviceCount, NULL));
	physicalDevices = (VkPhysicalDevice*)malloc(sizeof(VkPhysicalDevice*) * physicalDeviceCount);
	VK_CALL(vk.EnumeratePhysicalDevices(m_handle, &physicalDeviceCount, physicalDevices));

	for (int i = 0; i < physicalDeviceCount; i++) {
		m_physicalDevices.push_back(new VKLPhysicalDevice(physicalDevices[i], this));
	}

	free(physicalDevices);
*/
}

const VkAllocationCallbacks* VKLInstance::allocationCallbacks() const {
	return m_allocationCallbacks;
}

PFN_vkVoidFunction VKLInstance::procAddr(const char* name) const {
	return vkGetInstanceProcAddr(m_handle, name);
}

const std::vector<VKLPhysicalDevice*>& VKLInstance::getPhysicalDevices() const {
	return m_physicalDevices;
}
const std::vector<const char*>& VKLInstance::getLayers() const {
	return m_layers;
}

const std::vector<const char*>& VKLInstance::getExtensions() const {
	return m_extensions;
}

void VKLInstance::_destroy() {
	vkDestroyInstance(m_handle, m_allocationCallbacks);
}

VKLInstanceCreateInfo::VKLInstanceCreateInfo() {
	memset(&m_appInfo, 0, sizeof(VkApplicationInfo));
	memset(&m_createInfo, 0, sizeof(VkInstanceCreateInfo));
	
	m_appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
	m_appInfo.pApplicationName = "Hello Triangle";
    m_appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
    m_appInfo.pEngineName = "No Engine";
    m_appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
    m_appInfo.apiVersion = VK_MAKE_API_VERSION(0, 1, 2, 0);
	
	m_createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
	m_createInfo.pApplicationInfo = &m_appInfo;
	
	m_debug = VK_FALSE;
}

void VKLInstanceCreateInfo::printSelections() {
	if (!validate()) {
		printf("VKLInstanceCreateInfo not valid\n");
		return;
	}

	_printSelections();
}

void VKLInstanceCreateInfo::_printSelections() {
	printf("Layers:\n");
	for (uint32_t i = 0; i < supportedLayers.size(); ++i) {
		printf("\tLayer ");
		if (i < 10) {
			printf(" ");
		}
		printf(" %d: %s", i, supportedLayers[i].layerName);
		for (uint32_t j = 0; j < m_layers.size(); ++j) {
			if (strcmp(supportedLayers[i].layerName, m_layers[j]) == 0) {
				for (int k = 0; k < 50 - strlen(supportedLayers[i].layerName); k++) {
					printf(" ");
				}
				printf(" - Selected");
			}
		}
		printf("\n");
	}

	printf("Extensions:\n");
	for (uint32_t i = 0; i < supportedExtensions.size(); ++i) {
		printf("\tExtension ");
		if (i < 10) {
			printf(" ");
		}
		printf(" %d: %s", i, supportedExtensions[i].extensionName);
		for (uint32_t j = 0; j < m_extensions.size(); ++j) {
			if (strcmp(supportedExtensions[i].extensionName, m_extensions[j]) == 0) {
				for (int k = 0; k < 50 - strlen(supportedExtensions[i].extensionName); k++) {
					printf(" ");
				}
				printf(" - Selected");
			}
		}
		printf("\n");
	}
}

VKLInstanceCreateInfo& VKLInstanceCreateInfo::allocationCallbacks(VkAllocationCallbacks* allocationCallbacks) {
	m_allocationCallbacks = allocationCallbacks;
	return invalidate();
}

VKLInstanceCreateInfo& VKLInstanceCreateInfo::addLayer(const char* layer) {
	for (const char* lay : m_layers) {
		if (strcmp(lay, layer) == 0) {
			return invalidate();
		}
	}

	m_layers.push_back(layer);
	return invalidate();
}

VKLInstanceCreateInfo& VKLInstanceCreateInfo::addExtension(const char* extension) {
	for (const char* ext : m_extensions) {
		if (strcmp(ext, extension) == 0) {
			return invalidate();
		}
	}
	m_extensions.push_back(extension);
	return invalidate();
}

VKLInstanceCreateInfo& VKLInstanceCreateInfo::addExtensions(const char** extensions, uint32_t extensionCount) {
	for(int  i = 0; i < extensionCount; i++) {
		m_extensions.push_back(extensions[i]);
	}
	
	return invalidate();
}

VKLInstanceCreateInfo& VKLInstanceCreateInfo::debug(VkBool32 debug) {
	m_debug = debug;
	return invalidate();
}

bool VKLInstanceCreateInfo::supportsExtension(const char* extension) {
	if (!validate()) {
		printf("VKLInstanceCreateInfo not valid\n");
		return false;
	}
	
	return _supportsExtension(extension);
}

bool VKLInstanceCreateInfo::supportsLayer(const char* layer)  {
	if (!validate()) {
		printf("VKLInstanceCreateInfo not valid\n");
		return false;
	}
	return _supportsLayer(layer);
}

bool VKLInstanceCreateInfo::_supportsExtension(const char* extension) {
	for (int i = 0; i < supportedExtensions.size(); i++) {
		if (strcmp(supportedExtensions[i].extensionName, extension) == 0) {
			return true;
		}
	}

	return false;
}

bool VKLInstanceCreateInfo::_supportsLayer(const char* layer) {
	for (int i = 0; i < supportedLayers.size(); i++) {
		if (strcmp(supportedLayers[i].layerName, layer) == 0) {
			return true;
		}
	}

	return false;
}

bool VKLInstanceCreateInfo::_validate() {
	uint32_t layerCount = 0;
	vkEnumerateInstanceLayerProperties(&layerCount, NULL);
	supportedLayers.resize(layerCount);
	vkEnumerateInstanceLayerProperties(&layerCount, supportedLayers.data());

	uint32_t extensionCount = 0;
	vkEnumerateInstanceExtensionProperties(NULL, &extensionCount, NULL);
	supportedExtensions.resize(extensionCount);
	vkEnumerateInstanceExtensionProperties(NULL, &extensionCount, supportedExtensions.data());

#ifdef VKL_VALIDATION
	for (const char* lay : m_layers) {
		if (!_supportsLayer(lay)) {
			printf("VKL Validation Error: Layer '%s' is not supported by instance!\n", lay);
			return false;
		}
	}

	for (const char* ext : m_extensions) {
		if (!_supportsExtension(ext)) {
			printf("VKL Validation Error: Extension '%s' is not supported by instance!\n", ext);
			return false;
		}
	}
#endif

	if (_supportsExtension("VK_KHR_get_physical_device_properties2")) {
		addExtension("VK_KHR_get_physical_device_properties2");
	}

#ifdef VK_KHR_portability_enumeration

	if (_supportsExtension(VK_KHR_PORTABILITY_ENUMERATION_EXTENSION_NAME)) {
		addExtension(VK_KHR_PORTABILITY_ENUMERATION_EXTENSION_NAME);
		m_createInfo.flags = m_createInfo.flags | VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR;
	}

#endif

	if (m_debug) {
		if (_supportsLayer("VK_LAYER_KHRONOS_validation")) {
			addLayer("VK_LAYER_KHRONOS_validation");
		}

		if (_supportsLayer("VK_LAYER_LUNARG_monitor")) {
			addLayer("VK_LAYER_LUNARG_monitor");
		}

		if(_supportsExtension("VK_EXT_debug_utils")) {
			addExtension("VK_EXT_debug_utils");
		}

		//_printSelections();
	}

	

	m_createInfo.enabledLayerCount = m_layers.size();
	m_createInfo.ppEnabledLayerNames = m_layers.data();

	m_createInfo.enabledExtensionCount = m_extensions.size();
	m_createInfo.ppEnabledExtensionNames = m_extensions.data();

	return true;
}
