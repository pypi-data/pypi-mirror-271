#include <VKL/VKL.h>

VKLQueue::VKLQueue() {
	m_handle = (VkQueue)VK_NULL_HANDLE;
	m_device = NULL;
	m_familyIndex = -1;
}

void VKLQueue::init(const VKLDevice* device, VkQueue queue, uint32_t familyIndex) {
	m_handle = queue;
	m_device = device;
	m_familyIndex = familyIndex;
	
	m_cmdBuffer = new VKLCommandBuffer(this);
}

const VKLDevice* VKLQueue::device() const {
	return m_device;
}

VKLCommandBuffer* VKLQueue::getCmdBuffer() const {
	return m_cmdBuffer;
}

uint32_t VKLQueue::getFamilyIndex() const {
	return m_familyIndex;
}

void VKLQueue::submitAndWait(const VKLCommandBuffer* cmdBuffer) const {
	submitAndWait(cmdBuffer, 0, NULL, NULL);
}

void VKLQueue::submitAndWait(const VKLCommandBuffer* cmdBuffer, uint32_t waitSemaphoreCount, const VkSemaphore* pWaitSemaphores, const VkPipelineStageFlags* pWaitDstStageMask) const {
	submit(cmdBuffer, NULL, waitSemaphoreCount, pWaitSemaphores, pWaitDstStageMask);
	m_device->waitForFence(cmdBuffer->fence());
}

void VKLQueue::submit(const VKLCommandBuffer* cmdBuffer) const {
	submit(cmdBuffer, NULL, 0, NULL, NULL);
}

void VKLQueue::submit(const VKLCommandBuffer* cmdBuffer, const VkSemaphore* signalSempahore) const {
	submit(cmdBuffer, signalSempahore, 0, NULL, NULL);
}

void VKLQueue::submit(const VKLCommandBuffer* cmdBuffer, const VkSemaphore* signalSempahore, uint32_t waitSemaphoreCount, const VkSemaphore* pWaitSemaphores, const VkPipelineStageFlags* pWaitDstStageMask) const {
	VkSubmitInfo submitInfo;
	memset(&submitInfo, 0, sizeof(VkSubmitInfo));
	submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
	submitInfo.pNext = NULL;
	submitInfo.waitSemaphoreCount = waitSemaphoreCount;
	submitInfo.pWaitSemaphores = pWaitSemaphores;
	submitInfo.pWaitDstStageMask = pWaitDstStageMask;
	submitInfo.commandBufferCount = 1;
	submitInfo.pCommandBuffers = cmdBuffer->pHandle();
	submitInfo.signalSemaphoreCount = signalSempahore == NULL ? 0 : 1;
	submitInfo.pSignalSemaphores = signalSempahore;
	
	VK_CALL(m_device->vk.QueueSubmit(m_handle, 1, &submitInfo, cmdBuffer->fence()));
}

void VKLQueue::waitIdle() const {
	m_device->vk.QueueWaitIdle(m_handle);
}

void VKLQueue::destroy() {
	m_cmdBuffer->destroy();
}
