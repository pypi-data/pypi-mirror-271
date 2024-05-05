#include <VKL/VKL.h>

#include <algorithm>

VKLStaticAllocator::VKLStaticAllocator() {
    m_device = NULL;
    m_flags = 0;
    m_memory = (VkDeviceMemory)VK_NULL_HANDLE;
    m_size = 0;
}


VKLStaticAllocator::VKLStaticAllocator(const VKLDevice* device, VkMemoryPropertyFlags flags) {
    m_device = device;
    m_flags = flags;
    m_memory = (VkDeviceMemory)VK_NULL_HANDLE;
    m_size = 0;
}

void VKLStaticAllocator::create(const VKLDevice* device, VkMemoryPropertyFlags flags) {
    m_device = device;
    m_flags = flags;
}
    
int VKLStaticAllocator::registerMemoryRequirement(VkMemoryRequirements reqs) {
    m_requirements.push_back(reqs);
    return m_requirements.size() - 1;
}

int sort_function(std::pair<VkMemoryRequirements, int> a, std::pair<VkMemoryRequirements, int> b) {
    return a.first.alignment > b.first.alignment;
}

void VKLStaticAllocator::allocate() {
    if (m_memory != VK_NULL_HANDLE) {
        LOG_ERROR("VKLStaticAllocator::allocate: Memory already allocated");
        return;
    }

    uint32_t memoryTypeBits = 0xffffffff;
    for (int i = 0; i < m_requirements.size(); i++) {
        memoryTypeBits &= m_requirements[i].memoryTypeBits;
    }

    m_size = 0;

    std::vector<VkDeviceSize> og_sizes;
    og_sizes.resize(m_requirements.size());

    for (int i = 0; i < m_requirements.size(); i++) {
        og_sizes[i] = m_requirements[i].size;

        if(m_requirements[i].size % m_requirements[i].alignment != 0)
            m_requirements[i].size = (1 + (m_requirements[i].size / m_requirements[i].alignment)) * m_requirements[i].alignment;

        m_size += m_requirements[i].size;
    }
    
    VkMemoryAllocateInfo memoryAllocateInfo;
	memoryAllocateInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
	memoryAllocateInfo.pNext = NULL;
	memoryAllocateInfo.allocationSize = m_size;

	memoryAllocateInfo.memoryTypeIndex = -1;

	for (uint32_t i = 0; i < 32; ++i) {
		VkMemoryType memoryType = m_device->physical()->getMemoryProperties().memoryTypes[i];
		if (memoryTypeBits & 1) {
			if ((memoryType.propertyFlags & m_flags) == m_flags) {
				memoryAllocateInfo.memoryTypeIndex = i;
				break;
			}
		}
		memoryTypeBits = memoryTypeBits >> 1;
	}

	if(memoryAllocateInfo.memoryTypeIndex == -1) {
		LOG_ERROR("Error allocating memory!!!\n");
		return;
	}

	VK_CALL(m_device->vk.AllocateMemory(m_device->handle(), &memoryAllocateInfo, m_device->allocationCallbacks(), &m_memory));

    std::vector<std::pair<VkMemoryRequirements, int> > indexed_requirements;

    for (int i = 0; i < m_requirements.size(); i++) {
        indexed_requirements.push_back(std::make_pair(m_requirements[i], i));
    }

    std::sort(indexed_requirements.begin(), indexed_requirements.end(), sort_function);

    m_allocations.resize(m_requirements.size());

    VkDeviceSize offset = 0;
    for(int i = 0; i < m_requirements.size(); i++) {
        VkMemoryRequirements reqs = indexed_requirements[i].first;
        int index = indexed_requirements[i].second;

        m_allocations[index].offset = offset;
        m_allocations[index].size = og_sizes[index];
        m_allocations[index].memory = m_memory;

        LOG_INFO("Allocating %lu bytes at offset %lu with alignment %lu", og_sizes[index], offset, reqs.alignment);

        offset += reqs.size;
    }
}

VKLAllocation VKLStaticAllocator::getAllocation(int index) {
    return m_allocations[index];
}