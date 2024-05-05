#ifndef VKLStaticAllocator_h
#define VKLStaticAllocator_h

#include <VKL/VKL_base.h>

class VKLStaticAllocator {
public:
    VKLStaticAllocator();
    VKLStaticAllocator(const VKLDevice* device, VkMemoryPropertyFlags flags);

    void create(const VKLDevice* device, VkMemoryPropertyFlags flags);

    int registerMemoryRequirement(VkMemoryRequirements reqs);

    void allocate();

    VKLAllocation getAllocation(int index);
private:
    const VKLDevice* m_device;
    VkDeviceMemory m_memory;
    VkDeviceSize m_size;
    VkMemoryPropertyFlags m_flags;
    
    std::vector<VkMemoryRequirements> m_requirements;
    std::vector<VKLAllocation> m_allocations;
};

#endif