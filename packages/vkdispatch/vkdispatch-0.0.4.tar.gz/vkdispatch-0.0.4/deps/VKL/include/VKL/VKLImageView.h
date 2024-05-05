#ifndef VKLImageView_h
#define VKLImageView_h

#include <VKL/VKL_base.h>

class VKLImageViewCreateInfo : public VKLCreateInfo<VKLImageViewCreateInfo> {
public:
	VKLImageViewCreateInfo();

	VKLImageViewCreateInfo& image(const VKLImage* image);

	VKLImageViewCreateInfo& type(VkImageViewType type);
	VKLImageViewCreateInfo& format(VkFormat format);
private:
	VkImageViewCreateInfo m_createInfo;

	const VKLImage* m_image;

	bool _validate();

	friend class VKLImageView;
};

class VKLImageView : public VKLHandle<VkImageView>, public VKLCreator<VKLImageViewCreateInfo> {
public:
	VKLImageView();
	VKLImageView(const VKLImageViewCreateInfo& createInfo);

	const VKLImage* image() const;
private:
	const VKLDevice* m_device;
	const VKLImage* m_image;

	void _destroy();
	void _create(const VKLImageViewCreateInfo& createInfo);
};

#endif 