#ifdef VKL_SURFACE_WIN32
#define VK_USE_PLATFORM_WIN32_KHR
#endif

#ifdef VKL_SURFACE_MACOS
#define VK_USE_PLATFORM_METAL_EXT
#endif

#include <VKL/VKL.h>

VKLSurface::VKLSurface() : VKLCreator<VKLSurfaceCreateInfo>("VKLSurface") {
	m_instance = NULL;
}

VKLSurface::VKLSurface(const VKLSurfaceCreateInfo& createInfo) : VKLCreator<VKLSurfaceCreateInfo>("VKLSurface") {
	m_instance = NULL;
	create(createInfo);
}

void VKLSurface::_create(const VKLSurfaceCreateInfo& createInfo) {
	m_instance = createInfo.m_instance;

	switch (createInfo.m_type) {
	case VKL_SURFACE_CREATE_INFO_TYPE_HANDLE:
		m_handle = *(VkSurfaceKHR*)createInfo.m_createInfoPtr;
		break;
	case VKL_SURFACE_CREATE_INFO_TYPE_WIN32:
#ifdef VKL_SURFACE_WIN32
		((PFN_vkCreateWin32SurfaceKHR)m_instance->vk.CreateWin32SurfaceKHR)(m_instance->handle(), 
													(VkWin32SurfaceCreateInfoKHR*)createInfo.m_createInfoPtr, 
													m_instance->allocationCallbacks(), &m_handle);
#endif
		break;
	case VKL_SURFACE_CREATE_INFO_TYPE_MACOS:
#ifdef VKL_SURFACE_MACOS
	((PFN_vkCreateMetalSurfaceEXT)m_instance->vk.CreateMetalSurfaceEXT)(m_instance->handle(),
													(VkMetalSurfaceCreateInfoEXT*)createInfo.m_createInfoPtr,
													m_instance->allocationCallbacks(), &m_handle);
#endif
		break;
	default:
		break;
	}
}

void VKLSurface::_destroy() {
	vkDestroySurfaceKHR(m_instance->handle(), m_handle, m_instance->allocationCallbacks());
}

VKLSurfaceCreateInfo::VKLSurfaceCreateInfo() {
	m_createInfoPtr = NULL;
	m_type = VKL_SURFACE_CREATE_INFO_TYPE_UNDEFINED;
	m_instance = NULL;
}

VKLSurfaceCreateInfoHandle::VKLSurfaceCreateInfoHandle() {
	m_handle = (VkSurfaceKHR)VK_NULL_HANDLE;
	m_type = VKL_SURFACE_CREATE_INFO_TYPE_HANDLE;
}

VKLSurfaceCreateInfoHandle& VKLSurfaceCreateInfoHandle::handle(VkSurfaceKHR handle) {
	m_handle = handle;

	m_createInfoPtr = &m_handle;

	return (VKLSurfaceCreateInfoHandle&)invalidate();
}

VKLSurfaceCreateInfoHandle& VKLSurfaceCreateInfoHandle::instance(const VKLInstance* instance) {
	m_instance = instance;

	return (VKLSurfaceCreateInfoHandle&)invalidate();
}

bool VKLSurfaceCreateInfoHandle::_validate() {
	if (m_instance == NULL) {
		printf("VKL Validation Error: VKLSurfaceCreateInfoHandle::instance was not set!\n");
		return false;
	}

	if (m_handle == VK_NULL_HANDLE) {
		printf("VKL Validation Error: VKLSurfaceCreateInfoHandle::handle was not set!\n");
		return false;
	}

	return true;
}

#ifdef VKL_SURFACE_WIN32

VKLSurfaceCreateInfoWin32::VKLSurfaceCreateInfoWin32() {
	m_createInfoPtr = malloc(sizeof(VkWin32SurfaceCreateInfoKHR));
	m_type = VKL_SURFACE_CREATE_INFO_TYPE_WIN32;

	VkWin32SurfaceCreateInfoKHR* createInfo = (VkWin32SurfaceCreateInfoKHR*)m_createInfoPtr;

	createInfo->sType = VK_STRUCTURE_TYPE_WIN32_SURFACE_CREATE_INFO_KHR;
	createInfo->pNext = NULL;
	createInfo->flags = 0;
	createInfo->hinstance = GetModuleHandle(NULL);
	createInfo->hwnd = NULL;
}

VKLSurfaceCreateInfoWin32::~VKLSurfaceCreateInfoWin32() {
	free(m_createInfoPtr);
}

VKLSurfaceCreateInfoWin32& VKLSurfaceCreateInfoWin32::instance(const VKLInstance* instance) {
	m_instance = instance;

	return (VKLSurfaceCreateInfoWin32&)invalidate();
}

VKLSurfaceCreateInfoWin32& VKLSurfaceCreateInfoWin32::hinstance(void* hinstance) {
	VkWin32SurfaceCreateInfoKHR* createInfo = (VkWin32SurfaceCreateInfoKHR*)m_createInfoPtr;

	createInfo->hinstance = (HINSTANCE)hinstance;

	return (VKLSurfaceCreateInfoWin32&)invalidate();
}

VKLSurfaceCreateInfoWin32& VKLSurfaceCreateInfoWin32::hwnd(void* hwnd) {
	VkWin32SurfaceCreateInfoKHR* createInfo = (VkWin32SurfaceCreateInfoKHR*)m_createInfoPtr;

	createInfo->hwnd = (HWND)hwnd;

	return (VKLSurfaceCreateInfoWin32&)invalidate();
}

bool VKLSurfaceCreateInfoWin32::_validate() {
	if (m_instance == NULL) {
		printf("VKL Validation Error: VKLSurfaceCreateInfoWin32::instance was not set!\n");
		return false;
	}

	VkWin32SurfaceCreateInfoKHR* createInfo = (VkWin32SurfaceCreateInfoKHR*)m_createInfoPtr;

	if (createInfo->hwnd == NULL) {
		printf("VKL Validation Error: VKLSurfaceCreateInfoWin32::hwnd was not set!\n");
		return false;
	}

	return true;
}

#endif

#ifdef VKL_SURFACE_MACOS

VKLSurfaceCreateInfoMacOS::VKLSurfaceCreateInfoMacOS() {
	m_createInfoPtr = malloc(sizeof(VkMetalSurfaceCreateInfoEXT));
	m_type = VKL_SURFACE_CREATE_INFO_TYPE_MACOS;
	
	VkMetalSurfaceCreateInfoEXT* createInfo = (VkMetalSurfaceCreateInfoEXT*)m_createInfoPtr;
	
	createInfo->sType = VK_STRUCTURE_TYPE_METAL_SURFACE_CREATE_INFO_EXT;
	createInfo->pNext = NULL;
	createInfo->flags = 0;
	createInfo->pLayer = NULL;
}

VKLSurfaceCreateInfoMacOS::~VKLSurfaceCreateInfoMacOS() {
	free(m_createInfoPtr);
}

VKLSurfaceCreateInfoMacOS& VKLSurfaceCreateInfoMacOS::instance(const VKLInstance* instance) {
	m_instance = instance;
	
	return (VKLSurfaceCreateInfoMacOS&)invalidate();
}

VKLSurfaceCreateInfoMacOS& VKLSurfaceCreateInfoMacOS::caLayer(void* caLayer) {
	VkMetalSurfaceCreateInfoEXT* createInfo = (VkMetalSurfaceCreateInfoEXT*)m_createInfoPtr;
	
	createInfo->pLayer = caLayer;
	
	return (VKLSurfaceCreateInfoMacOS&)invalidate();
}

bool VKLSurfaceCreateInfoMacOS::_validate() {
	if(m_instance == NULL) {
		printf("VKL Validation Error: VKLSurfaceCreateInfoMacOS::instance was not set!\n");
		return false;
	}
	
	VkMetalSurfaceCreateInfoEXT* createInfo = (VkMetalSurfaceCreateInfoEXT*)m_createInfoPtr;
	
	if(createInfo->pLayer == NULL) {
		printf("VKL Validation Error: VKLSurfaceCreateInfoMacOS::caLayer was not set!\n");
		return false;
	}
	
	return true;
}

#endif

