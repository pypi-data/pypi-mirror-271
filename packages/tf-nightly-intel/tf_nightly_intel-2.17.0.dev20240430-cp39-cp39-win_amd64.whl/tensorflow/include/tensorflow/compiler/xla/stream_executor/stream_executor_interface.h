/* Copyright 2024 The OpenXLA Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_STREAM_EXECUTOR_STREAM_EXECUTOR_INTERFACE_H_
#define XLA_STREAM_EXECUTOR_STREAM_EXECUTOR_INTERFACE_H_

#include <cstdint>
#include <memory>
#include <optional>

#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "absl/types/span.h"
#include "xla/stream_executor/allocator_stats.h"
#include "xla/stream_executor/blas.h"
#include "xla/stream_executor/command_buffer.h"
#include "xla/stream_executor/device_memory.h"
#include "xla/stream_executor/dnn.h"
#include "xla/stream_executor/event.h"
#include "xla/stream_executor/fft.h"
#include "xla/stream_executor/kernel.h"
#include "xla/stream_executor/kernel_spec.h"
#include "xla/stream_executor/launch_dim.h"
#include "xla/stream_executor/memory_allocation.h"
#include "xla/stream_executor/module_spec.h"
#include "xla/stream_executor/stream_interface.h"

namespace stream_executor {

class Stream;

// Interface which defines the method for interacting with an accelerator device
// (e.g. GPU, TPU).
class StreamExecutorInterface {
 public:
  StreamExecutorInterface() = default;
  virtual ~StreamExecutorInterface() = default;

  // Initializes the device for use.
  virtual absl::Status Init() = 0;

  // Returns the device ordinal.
  virtual int device_ordinal() const { return -1; }

  // Retrieves (loads) a kernel, if one exists.
  //
  // Parameters:
  //   spec: The MultiKernelLoaderSpec is usually generated as a compile-time
  //    constant into an appropriate namespace.
  //   kernel: Outparam that the kernel is loaded into. A given Kernel
  //    instantiation should not be loaded into more than once.
  virtual absl::Status GetKernel(const MultiKernelLoaderSpec& spec,
                                 Kernel* kernel) {
    return absl::UnimplementedError("Not Implemented");
  }

  // Unloads the module with handle `module_handle`.
  virtual bool UnloadModule(ModuleHandle module_handle) { return false; }

  // Loads a module for the platform this StreamExecutor is acting upon.
  //
  // `spec` describes the module to be loaded.  On success writes the handle for
  // the loaded module to `module_handle` and returns OkStatus().  Otherwise,
  // returns the error which has occurred.
  virtual absl::Status LoadModule(const MultiModuleLoaderSpec& spec,
                                  ModuleHandle* module_handle) {
    return absl::UnimplementedError("Not Implemented");
  }

  // Creates a shared constant using the content provided.
  virtual absl::StatusOr<std::shared_ptr<DeviceMemoryBase>>
  CreateOrShareConstant(Stream* stream, absl::Span<const uint8_t> content) {
    return absl::UnimplementedError("Not Implemented");
  }

  // Launches a data parallel kernel with the given thread/block
  // dimensionality and already-packed args/sizes to pass to the underlying
  // platform driver.

  virtual absl::Status Launch(Stream* stream, const ThreadDim& thread_dims,
                              const BlockDim& block_dims, const Kernel& k,
                              const KernelArgs& args) {
    return absl::UnimplementedError("Not Implemented");
  }

  // Launches a data parallel kernel with the given thread/block
  // dimensionality and already-packed args/sizes to pass to the underlying
  // platform driver.
  virtual absl::Status Launch(Stream* stream, const ThreadDim& thread_dims,
                              const BlockDim& block_dims,
                              const ClusterDim& cluster_dims, const Kernel& k,
                              const KernelArgs& args) {
    return absl::UnimplementedError("Not Implemented");
  }

  // Submits command buffer for execution to the underlying platform driver.
  virtual absl::Status Submit(Stream* stream,
                              const CommandBuffer& command_buffer) {
    return absl::UnimplementedError("Not Implemented");
  }

  // Releases any state associated with the previously loaded kernel.
  virtual void UnloadKernel(const Kernel* kernel) {}

  // Synchronously allocates size bytes on the underlying platform and returns
  // a DeviceMemoryBase representing that allocation. In the case of failure,
  // nullptr is returned.
  virtual DeviceMemoryBase Allocate(uint64_t size, int64_t memory_space) = 0;
  DeviceMemoryBase Allocate(uint64_t size) {
    return Allocate(size, /*memory_space=*/0);
  }
  // Deallocates the DeviceMemory previously allocated via this interface.
  // Deallocation of a nullptr-representative value is permitted.
  virtual void Deallocate(DeviceMemoryBase* mem) = 0;

  // Allocates unified memory space of the given size, if supported.
  // See
  // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#um-unified-memory-programming-hd
  // for more details on unified memory.
  virtual void* UnifiedMemoryAllocate(uint64_t size) { return nullptr; }

  // Deallocates unified memory space previously allocated with
  // UnifiedMemoryAllocate.
  virtual void UnifiedMemoryDeallocate(void* mem) {}

  // Allocates collective device memory using ncclMemAlloc.
  // See
  // https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/bufferreg.html
  // for more details on User Buffer Registration.
  virtual absl::StatusOr<void*> CollectiveMemoryAllocate(uint64_t size) {
    return absl::UnimplementedError("Not implemented");
  }

  // Deallocates collective device memory previously allocated with
  // CollectiveMemoryAllocate.
  virtual absl::Status CollectiveMemoryDeallocate(void* mem) {
    return absl::UnimplementedError("Not implemented");
  }

  // Allocates a region of host memory and registers it with the platform API.
  // Memory allocated in this manner is required for use in asynchronous memcpy
  // operations, such as Stream::Memcpy.
  virtual absl::StatusOr<std::unique_ptr<MemoryAllocation>> HostMemoryAllocate(
      uint64_t size) = 0;

  // Deallocates a region of host memory allocated by HostMemoryAllocate().
  virtual void HostMemoryDeallocate(void* mem) = 0;

  // Synchronizes all activity occurring in the StreamExecutor's context.
  virtual bool SynchronizeAllActivity() = 0;

  // Blocks the caller while "size" bytes are zeroed out (in POD fashion) at the
  // given location in device memory.
  virtual absl::Status SynchronousMemZero(DeviceMemoryBase* location,
                                          uint64_t size) = 0;

  // Blocks the caller while "size" bytes are copied to the given location in
  // device memory.
  virtual absl::Status SynchronousMemcpy(DeviceMemoryBase* device_dst,
                                         const void* host_src,
                                         uint64_t size) = 0;

  // Blocks the caller while "size" bytes are copied to the given location in
  // host memory.
  virtual absl::Status SynchronousMemcpy(void* host_dst,
                                         const DeviceMemoryBase& device_src,
                                         uint64_t size) = 0;

  // Enqueues an operation onto stream to zero out size bytes at the given
  // device memory location. Neither stream nor location may be null. Returns
  // whether the operation was successfully enqueued onto the stream.
  virtual absl::Status MemZero(Stream* stream, DeviceMemoryBase* location,
                               uint64_t size) = 0;

  // Enqueues an operation onto stream to set 8-bit patterns starting at
  // location, for byte count given by size.  Returns whether the operation was
  // successfully enqueued onto the stream.
  virtual absl::Status Memset(Stream* stream, DeviceMemoryBase* location,
                              uint8 pattern, uint64_t size) {
    return absl::InternalError("Not implemented");
  }

  // Enqueues an operation onto stream to set 32-bit patterns starting at
  // location, for byte count given by size. size must be 32-bit quantified
  // (i.e. evenly divisible by 4). Returns whether the operation was
  // successfully enqueued onto the stream.
  virtual absl::Status Memset32(Stream* stream, DeviceMemoryBase* location,
                                uint32_t pattern, uint64_t size) = 0;

  // Enqueues a memcpy operation onto stream, with a host destination location
  // host_dst and a device memory source, with target size size.
  virtual absl::Status Memcpy(Stream* stream, void* host_dst,
                              const DeviceMemoryBase& device_src,
                              uint64_t size) = 0;

  // Enqueues a memcpy operation onto stream, with a device destination location
  // and a host memory source, with target size size.
  virtual absl::Status Memcpy(Stream* stream, DeviceMemoryBase* device_dst,
                              const void* host_src, uint64_t size) = 0;

  // Enqueues a memcpy operation onto stream, with a device destination location
  // and a device source location, with target size size. Peer access should
  // have been enabled between the StreamExecutors owning the device memory
  // regions.
  virtual bool MemcpyDeviceToDevice(Stream* stream,
                                    DeviceMemoryBase* device_dst,
                                    const DeviceMemoryBase& device_src,
                                    uint64_t size) = 0;

  // Enqueues on a stream a user-specified function to be run on the host.
  virtual bool HostCallback(Stream* stream,
                            absl::AnyInvocable<absl::Status() &&> callback) = 0;

  // Performs platform-specific allocation and initialization of an event.
  virtual absl::Status AllocateEvent(Event* event) = 0;

  // Performs platform-specific deallocation and cleanup of an event.
  virtual absl::Status DeallocateEvent(Event* event) = 0;

  // Inserts the specified event at the end of the specified stream.
  virtual absl::Status RecordEvent(Stream* stream, Event* event) = 0;

  // Waits for the specified event at the end of the specified stream.
  virtual absl::Status WaitForEvent(Stream* stream, Event* event) = 0;

  // Waits for the specified event at the end of the raw platform-specific
  // stream.
  virtual absl::Status WaitForEventOnExternalStream(std::intptr_t stream,
                                                    Event* event) {
    return absl::UnimplementedError(
        "WaitForEventOnExternalStream not supported on this executor.");
  }

  // Requests the current status of the event from the underlying platform.
  virtual Event::Status PollForEventStatus(Event* event) = 0;

  // Allocates stream resources on the underlying platform and initializes its
  // internals.
  virtual bool AllocateStream(Stream* stream) = 0;

  // Deallocates stream resources on the underlying platform.
  virtual void DeallocateStream(Stream* stream) = 0;

  // Causes dependent to not begin execution until other has finished its
  // last-enqueued work.
  virtual bool CreateStreamDependency(Stream* dependent, Stream* other) = 0;

  // Causes the host code to synchronously wait for operations enqueued
  // onto stream to complete. Effectively a join on the asynchronous device
  // operations enqueued on the stream before this program point.
  virtual absl::Status BlockHostUntilDone(Stream* stream) = 0;

  // Without blocking the device, retrieve the current stream status.
  virtual absl::Status GetStatus(Stream* stream) {
    return absl::UnimplementedError(
        "GetStatus is not supported on this executor.");
  }
  // Enables peer access from this StreamExecutor to memory
  // allocated by other, such that launched device code, memcpies, etc may
  // access it directly.
  virtual absl::Status EnablePeerAccessTo(StreamExecutorInterface* other) = 0;

  // Returns whether it's possible to enable peer access from this
  // StreamExecutor to memory allocated by another.
  virtual bool CanEnablePeerAccessTo(StreamExecutorInterface* other) = 0;

  // Returns the underlying device memory usage information, if it is available.
  // If it is not available (false is returned), free/total may not be
  // initialized.
  virtual bool DeviceMemoryUsage(int64_t* free, int64_t* total) const {
    return false;
  }

  // Retrieves device pointer and size for a symbol. The device pointer is
  // stored at mem, and the size is stored at size. Either mem or bytes can be
  // null, however, both of them cannot be null at the same time. To use
  // constant memory in CUDA, GetSymbol has to be used. Returns true if symbol
  // is found.
  //
  // If ModuleHandle is set then we search for `symbol_name` only within the
  // module corresponding to `module_handle`.  Otherwise all loaded modules are
  // searched.
  virtual bool GetSymbol(const std::string& symbol_name,
                         ModuleHandle module_handle, void** mem,
                         size_t* bytes) {
    return false;
  }

  // Creates a new DeviceDescription object. Ownership is transferred to the
  // caller.
  virtual absl::StatusOr<std::unique_ptr<DeviceDescription>>
  CreateDeviceDescription() const = 0;

  // Gets-or-creates a BlasSupport datatype that can be used to execute BLAS
  // routines on the current platform.
  //
  // Returns null if there was an error initializing the BLAS support for the
  // underlying platform.
  virtual blas::BlasSupport* AsBlas() { return nullptr; }

  // Gets or creates a FftSupport datatype that can be used to execute FFT
  // routines on the current platform.
  //
  // Returns null if there was an error initializing the FFT support for the
  // underlying platform.
  virtual fft::FftSupport* AsFft() { return nullptr; }

  // Gets-or-creates  a DnnSupport datatype that can be used for neural network
  // routines on the current platform.
  //
  // Returns null if there was an error initializing the DNN support for the
  // underlying platform.
  virtual dnn::DnnSupport* AsDnn() { return nullptr; }

  // Each call creates a new instance of the platform-specific implementation of
  // the corresponding interface type.
  virtual std::unique_ptr<EventInterface> CreateEventImplementation() = 0;
  virtual std::unique_ptr<StreamInterface> GetStreamImplementation() = 0;

  // Creates a new Kernel object.
  // TODO(klucke) Combine with GetKernel.
  virtual absl::StatusOr<std::unique_ptr<Kernel>> CreateKernel() {
    return absl::UnimplementedError("Kernels are not implemented");
  }

  // Creates a new CommandBuffer object.
  virtual absl::StatusOr<std::unique_ptr<CommandBuffer>> CreateCommandBuffer(
      CommandBuffer::Mode mode) {
    return absl::UnimplementedError("Command buffers are not implemented");
  }

  // Returns allocator statistics.
  virtual std::optional<AllocatorStats> GetAllocatorStats() {
    return std::nullopt;
  }

  // Clears the internal stats except for the `in_use` fields  and sets the
  // `peak_bytes_in_use` to be equal to the `bytes_in_use`. Returns true if
  // implemented.
  virtual bool ClearAllocatorStats() { return false; }

  // Clears the compilation cache from volatile memory. Returns OK if no
  // compilation cache exists or if clearing the compilation cache is
  // unsupported. Caches in non-volatile storage are unaffected.
  virtual absl::Status FlushCompilationCache() { return absl::OkStatus(); }

  // Returns a stream allocated by this executor, or nullptr if not found.
  virtual Stream* FindAllocatedStream(void* device_stream) { return nullptr; }

 private:
  StreamExecutorInterface(const StreamExecutorInterface&) = delete;
  void operator=(const StreamExecutorInterface&) = delete;
};

}  // namespace stream_executor

#endif  // XLA_STREAM_EXECUTOR_STREAM_EXECUTOR_INTERFACE_H_
