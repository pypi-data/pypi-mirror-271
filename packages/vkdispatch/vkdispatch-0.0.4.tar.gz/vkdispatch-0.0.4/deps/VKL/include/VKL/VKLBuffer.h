//
//  VKLBuffer.h
//  VKL
//
//  Created by Shahar Sandhaus on 7/22/21.
//

#ifndef VKLBuffer_h
#define VKLBuffer_h

#include "VKL_base.h"

class VKLBufferCreateInfo : public VKLCreateInfo<VKLBufferCreateInfo> {
public:
	VKLBufferCreateInfo();

	VKLBufferCreateInfo& pNext(void* pNext);
	
	VKLBufferCreateInfo& device(const VKLDevice* device);
	VKLBufferCreateInfo& size(VkDeviceSize size);
	VKLBufferCreateInfo& usage(VkBufferUsageFlags usage);

	VKLBufferCreateInfo& useVMA(bool useVMA);
	VKLBufferCreateInfo& usageVMA(VmaMemoryUsage usage);
	VKLBufferCreateInfo& flagsVMA(VmaAllocationCreateFlags flags);
	
	VKLBufferCreateInfo& memoryProperties(VkMemoryPropertyFlags memoryProperties);
	
private:
	VkBufferCreateInfo m_bufferCreateInfo;	
	const VKLDevice* m_device;
	bool useVMAFlag;
	VmaMemoryUsage usageVMAFlag;
	VmaAllocationCreateFlags flagsVMAFlag;

	bool _validate();

	friend class VKLBuffer;
};

class VKLBuffer : public VKLHandle<VkBuffer>, public VKLCreator<VKLBufferCreateInfo> {
public:
	VKLBuffer();
	VKLBuffer(const VKLBufferCreateInfo& createInfo);

	void bind(VKLAllocation allocation);

	VKLAllocation allocation() const;
	VkMemoryRequirements memoryRequirements() const;
	
	void* map();
	void unmap();
	
	void setData(void* data, size_t size, size_t offset);
	void getData(void* data, size_t size, size_t offset);
	
	void setNewAccessMask(VkAccessFlags accessMask);
	VkBufferMemoryBarrier* getMemoryBarrier();
	void resetBarrier();
	
	void copyFrom(VKLBuffer* src, const VKLQueue* transferQueue, VkBufferCopy bufferCopy);
	void uploadData(const VKLQueue* transferQueue, void* data, size_t size, size_t offset);
	void downloadData(const VKLQueue* transferQueue, void* data, size_t size, size_t offset);
private:
	const VKLDevice* m_device;
	
	VKLAllocation m_allocation;

	VkBufferMemoryBarrier m_memoryBarrier;
	
	void _destroy();
	void _create(const VKLBufferCreateInfo& createInfo);
};

#endif /* VKLBuffer_h */
