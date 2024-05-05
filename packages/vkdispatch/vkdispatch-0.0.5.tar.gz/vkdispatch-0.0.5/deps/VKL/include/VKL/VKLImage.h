#ifndef VKLImage_h
#define VKLImage_h

#include "VKL_base.h"

class VKLImageCreateInfo : public VKLCreateInfo<VKLImageCreateInfo>  {
public:
	VKLImageCreateInfo();
	
	VKLImageCreateInfo& device(const VKLDevice* device);

	VKLImageCreateInfo& pNext(void* pNext);

	VKLImageCreateInfo& allocationPNext(void* pNext);
	
	VKLImageCreateInfo& imageType(VkImageType type);
	VKLImageCreateInfo& format(VkFormat format);
	VKLImageCreateInfo& extent(uint32_t width, uint32_t height, uint32_t depth);
	VKLImageCreateInfo& tiling(VkImageTiling tiling);
	VKLImageCreateInfo& usage(VkImageUsageFlags usage);
	VKLImageCreateInfo& initialLayout(VkImageLayout layout);

	VKLImageCreateInfo& arrayLayers(uint32_t arrayLayers);
	
	VKLImageCreateInfo& memoryProperties(VkMemoryPropertyFlags memoryProperties);	

	VKLImageCreateInfo& useVMA(bool useVMA);
	VKLImageCreateInfo& usageVMA(VmaMemoryUsage usage);
	VKLImageCreateInfo& flagsVMA(VmaAllocationCreateFlags flags);

private:
	VkImageCreateInfo m_imageCreateInfo;
	void* m_allocationPNext;
	VkMemoryPropertyFlags m_memoryProperties;
	const VKLDevice* m_device;

	bool useVMAFlag;
	VmaMemoryUsage usageVMAFlag;
	VmaAllocationCreateFlags flagsVMAFlag;

	bool _validate();

	friend class VKLImage;
};

class VKLImage : public VKLHandle<VkImage>, public VKLCreator<VKLImageCreateInfo> {
public:
	VKLImage();
	VKLImage(const VKLImageCreateInfo& createInfo);

	void bind(VKLAllocation allocation);
	
	VkAccessFlags accessMask() const;
	VkImageLayout layout() const;
	
	VkExtent3D extent() const;
	VkImageAspectFlags aspect() const;

	int layers() const;

	VKLAllocation allocation() const;

	VkMemoryRequirements memoryRequirements() const;
	
	void transition(const VKLQueue* queue, VkAccessFlags accessMask, VkImageLayout layout, VkPipelineStageFlags srcStageMask, VkPipelineStageFlags dstStageMask);
	void cmdTransitionBarrier(VKLCommandBuffer* cmdBuffer, VkAccessFlags accessMask, VkImageLayout layout, VkPipelineStageFlags srcStageMask, VkPipelineStageFlags dstStageMask);

	void copyFrom(VKLImage* src, const VKLQueue* transferQueue, VkImageCopy imageCopy);
	void setData(void* data, size_t size, size_t pixelSize);
	void getData(void* data, size_t size, size_t pixelSize);
	void uploadData(const VKLQueue* transferQueue, void* data, size_t size, size_t pixelSize);
	
	void uploadDataBuffer(const VKLQueue* transferQueue, void* data, size_t size);
	void downloadDataBuffer(const VKLQueue* transferQueue, void* data, size_t size);

	VkFormat format() const;
	
	VkImageAspectFlags m_aspect;
private:
	VkImageMemoryBarrier m_memoryBarrier;
	VKLAllocation m_allocation;

	VkFormat m_format;
	
	VkExtent3D m_size;
	int m_layers;

	void initBarrier(VkImageLayout layout);

	const VKLDevice* m_device;
	
	void _destroy();
	void _create(const VKLImageCreateInfo& createInfo);
	void _create(const VKLImageCreateInfo& createInfo, VkImage handle);

	friend class VKLImageView;
	friend class VKLSwapChain;
};

#endif
