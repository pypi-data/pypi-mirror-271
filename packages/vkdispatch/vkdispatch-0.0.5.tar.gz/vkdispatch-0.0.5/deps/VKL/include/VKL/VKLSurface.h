#ifndef VKLSurface_h
#define VKLSurface_h

#include <VKL/VKL_base.h>

typedef enum {
	VKL_SURFACE_CREATE_INFO_TYPE_UNDEFINED = 0,
	VKL_SURFACE_CREATE_INFO_TYPE_HANDLE = 1,
	VKL_SURFACE_CREATE_INFO_TYPE_WIN32 = 2,
	VKL_SURFACE_CREATE_INFO_TYPE_MACOS = 3,
} VKLSurfaceCreateInfoType;

class VKLSurfaceCreateInfo : public VKLCreateInfo<VKLSurfaceCreateInfo> {
protected:
	VKLSurfaceCreateInfo();

	const VKLInstance* m_instance;

	VKLSurfaceCreateInfoType m_type;
	void* m_createInfoPtr;

	friend class VKLSurface;
};

class VKLSurfaceCreateInfoHandle : public VKLSurfaceCreateInfo {
public:
	VKLSurfaceCreateInfoHandle();

	VKLSurfaceCreateInfoHandle& handle(VkSurfaceKHR handle);
	VKLSurfaceCreateInfoHandle& instance(const VKLInstance* instance);

private:
	bool _validate();

	VkSurfaceKHR m_handle;
};

#ifdef VKL_SURFACE_WIN32

class VKLSurfaceCreateInfoWin32 : public VKLSurfaceCreateInfo {
public:
	VKLSurfaceCreateInfoWin32();
	~VKLSurfaceCreateInfoWin32();

	VKLSurfaceCreateInfoWin32& instance(const VKLInstance* instance);
	VKLSurfaceCreateInfoWin32& hinstance(void* hinstance);
	VKLSurfaceCreateInfoWin32& hwnd(void* hwnd);

private:
	bool _validate();
};

#endif

#ifdef VKL_SURFACE_MACOS

class VKLSurfaceCreateInfoMacOS : public VKLSurfaceCreateInfo {
public:
	VKLSurfaceCreateInfoMacOS();
	~VKLSurfaceCreateInfoMacOS();

	VKLSurfaceCreateInfoMacOS& instance(const VKLInstance* instance);
	VKLSurfaceCreateInfoMacOS& caLayer(void* caLayer);

private:
	bool _validate();
};

#endif

class VKLSurface : public VKLHandle<VkSurfaceKHR>, public VKLCreator<VKLSurfaceCreateInfo> {
public:
	VKLSurface();
	VKLSurface(const VKLSurfaceCreateInfo& createInfo);
private:
	const VKLInstance* m_instance;

	void _create(const VKLSurfaceCreateInfo& createInfo);
	void _destroy();
};

#endif
