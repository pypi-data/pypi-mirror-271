// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: xla/pjrt/cpu/cpu_topology.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto;
namespace xla {
class CpuTopologyProto;
struct CpuTopologyProtoDefaultTypeInternal;
extern CpuTopologyProtoDefaultTypeInternal _CpuTopologyProto_default_instance_;
class CpuTopologyProto_CpuDevice;
struct CpuTopologyProto_CpuDeviceDefaultTypeInternal;
extern CpuTopologyProto_CpuDeviceDefaultTypeInternal _CpuTopologyProto_CpuDevice_default_instance_;
}  // namespace xla
PROTOBUF_NAMESPACE_OPEN
template<> ::xla::CpuTopologyProto* Arena::CreateMaybeMessage<::xla::CpuTopologyProto>(Arena*);
template<> ::xla::CpuTopologyProto_CpuDevice* Arena::CreateMaybeMessage<::xla::CpuTopologyProto_CpuDevice>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace xla {

// ===================================================================

class CpuTopologyProto_CpuDevice final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.CpuTopologyProto.CpuDevice) */ {
 public:
  inline CpuTopologyProto_CpuDevice() : CpuTopologyProto_CpuDevice(nullptr) {}
  ~CpuTopologyProto_CpuDevice() override;
  explicit PROTOBUF_CONSTEXPR CpuTopologyProto_CpuDevice(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  CpuTopologyProto_CpuDevice(const CpuTopologyProto_CpuDevice& from);
  CpuTopologyProto_CpuDevice(CpuTopologyProto_CpuDevice&& from) noexcept
    : CpuTopologyProto_CpuDevice() {
    *this = ::std::move(from);
  }

  inline CpuTopologyProto_CpuDevice& operator=(const CpuTopologyProto_CpuDevice& from) {
    CopyFrom(from);
    return *this;
  }
  inline CpuTopologyProto_CpuDevice& operator=(CpuTopologyProto_CpuDevice&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const CpuTopologyProto_CpuDevice& default_instance() {
    return *internal_default_instance();
  }
  static inline const CpuTopologyProto_CpuDevice* internal_default_instance() {
    return reinterpret_cast<const CpuTopologyProto_CpuDevice*>(
               &_CpuTopologyProto_CpuDevice_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(CpuTopologyProto_CpuDevice& a, CpuTopologyProto_CpuDevice& b) {
    a.Swap(&b);
  }
  inline void Swap(CpuTopologyProto_CpuDevice* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(CpuTopologyProto_CpuDevice* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  CpuTopologyProto_CpuDevice* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<CpuTopologyProto_CpuDevice>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const CpuTopologyProto_CpuDevice& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const CpuTopologyProto_CpuDevice& from) {
    CpuTopologyProto_CpuDevice::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(CpuTopologyProto_CpuDevice* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.CpuTopologyProto.CpuDevice";
  }
  protected:
  explicit CpuTopologyProto_CpuDevice(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kIdFieldNumber = 1,
    kProcessIndexFieldNumber = 2,
    kLocalHardwareIdFieldNumber = 3,
  };
  // int32 id = 1;
  void clear_id();
  int32_t id() const;
  void set_id(int32_t value);
  private:
  int32_t _internal_id() const;
  void _internal_set_id(int32_t value);
  public:

  // int32 process_index = 2;
  void clear_process_index();
  int32_t process_index() const;
  void set_process_index(int32_t value);
  private:
  int32_t _internal_process_index() const;
  void _internal_set_process_index(int32_t value);
  public:

  // int32 local_hardware_id = 3;
  void clear_local_hardware_id();
  int32_t local_hardware_id() const;
  void set_local_hardware_id(int32_t value);
  private:
  int32_t _internal_local_hardware_id() const;
  void _internal_set_local_hardware_id(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:xla.CpuTopologyProto.CpuDevice)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    int32_t id_;
    int32_t process_index_;
    int32_t local_hardware_id_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto;
};
// -------------------------------------------------------------------

class CpuTopologyProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.CpuTopologyProto) */ {
 public:
  inline CpuTopologyProto() : CpuTopologyProto(nullptr) {}
  ~CpuTopologyProto() override;
  explicit PROTOBUF_CONSTEXPR CpuTopologyProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  CpuTopologyProto(const CpuTopologyProto& from);
  CpuTopologyProto(CpuTopologyProto&& from) noexcept
    : CpuTopologyProto() {
    *this = ::std::move(from);
  }

  inline CpuTopologyProto& operator=(const CpuTopologyProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline CpuTopologyProto& operator=(CpuTopologyProto&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const CpuTopologyProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const CpuTopologyProto* internal_default_instance() {
    return reinterpret_cast<const CpuTopologyProto*>(
               &_CpuTopologyProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(CpuTopologyProto& a, CpuTopologyProto& b) {
    a.Swap(&b);
  }
  inline void Swap(CpuTopologyProto* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(CpuTopologyProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  CpuTopologyProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<CpuTopologyProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const CpuTopologyProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const CpuTopologyProto& from) {
    CpuTopologyProto::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(CpuTopologyProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.CpuTopologyProto";
  }
  protected:
  explicit CpuTopologyProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  typedef CpuTopologyProto_CpuDevice CpuDevice;

  // accessors -------------------------------------------------------

  enum : int {
    kCpuDevicesFieldNumber = 1,
    kMachineAttributesFieldNumber = 4,
  };
  // repeated .xla.CpuTopologyProto.CpuDevice cpu_devices = 1;
  int cpu_devices_size() const;
  private:
  int _internal_cpu_devices_size() const;
  public:
  void clear_cpu_devices();
  ::xla::CpuTopologyProto_CpuDevice* mutable_cpu_devices(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::CpuTopologyProto_CpuDevice >*
      mutable_cpu_devices();
  private:
  const ::xla::CpuTopologyProto_CpuDevice& _internal_cpu_devices(int index) const;
  ::xla::CpuTopologyProto_CpuDevice* _internal_add_cpu_devices();
  public:
  const ::xla::CpuTopologyProto_CpuDevice& cpu_devices(int index) const;
  ::xla::CpuTopologyProto_CpuDevice* add_cpu_devices();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::CpuTopologyProto_CpuDevice >&
      cpu_devices() const;

  // repeated string machine_attributes = 4;
  int machine_attributes_size() const;
  private:
  int _internal_machine_attributes_size() const;
  public:
  void clear_machine_attributes();
  const std::string& machine_attributes(int index) const;
  std::string* mutable_machine_attributes(int index);
  void set_machine_attributes(int index, const std::string& value);
  void set_machine_attributes(int index, std::string&& value);
  void set_machine_attributes(int index, const char* value);
  void set_machine_attributes(int index, const char* value, size_t size);
  std::string* add_machine_attributes();
  void add_machine_attributes(const std::string& value);
  void add_machine_attributes(std::string&& value);
  void add_machine_attributes(const char* value);
  void add_machine_attributes(const char* value, size_t size);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>& machine_attributes() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>* mutable_machine_attributes();
  private:
  const std::string& _internal_machine_attributes(int index) const;
  std::string* _internal_add_machine_attributes();
  public:

  // @@protoc_insertion_point(class_scope:xla.CpuTopologyProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::CpuTopologyProto_CpuDevice > cpu_devices_;
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string> machine_attributes_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// CpuTopologyProto_CpuDevice

// int32 id = 1;
inline void CpuTopologyProto_CpuDevice::clear_id() {
  _impl_.id_ = 0;
}
inline int32_t CpuTopologyProto_CpuDevice::_internal_id() const {
  return _impl_.id_;
}
inline int32_t CpuTopologyProto_CpuDevice::id() const {
  // @@protoc_insertion_point(field_get:xla.CpuTopologyProto.CpuDevice.id)
  return _internal_id();
}
inline void CpuTopologyProto_CpuDevice::_internal_set_id(int32_t value) {
  
  _impl_.id_ = value;
}
inline void CpuTopologyProto_CpuDevice::set_id(int32_t value) {
  _internal_set_id(value);
  // @@protoc_insertion_point(field_set:xla.CpuTopologyProto.CpuDevice.id)
}

// int32 process_index = 2;
inline void CpuTopologyProto_CpuDevice::clear_process_index() {
  _impl_.process_index_ = 0;
}
inline int32_t CpuTopologyProto_CpuDevice::_internal_process_index() const {
  return _impl_.process_index_;
}
inline int32_t CpuTopologyProto_CpuDevice::process_index() const {
  // @@protoc_insertion_point(field_get:xla.CpuTopologyProto.CpuDevice.process_index)
  return _internal_process_index();
}
inline void CpuTopologyProto_CpuDevice::_internal_set_process_index(int32_t value) {
  
  _impl_.process_index_ = value;
}
inline void CpuTopologyProto_CpuDevice::set_process_index(int32_t value) {
  _internal_set_process_index(value);
  // @@protoc_insertion_point(field_set:xla.CpuTopologyProto.CpuDevice.process_index)
}

// int32 local_hardware_id = 3;
inline void CpuTopologyProto_CpuDevice::clear_local_hardware_id() {
  _impl_.local_hardware_id_ = 0;
}
inline int32_t CpuTopologyProto_CpuDevice::_internal_local_hardware_id() const {
  return _impl_.local_hardware_id_;
}
inline int32_t CpuTopologyProto_CpuDevice::local_hardware_id() const {
  // @@protoc_insertion_point(field_get:xla.CpuTopologyProto.CpuDevice.local_hardware_id)
  return _internal_local_hardware_id();
}
inline void CpuTopologyProto_CpuDevice::_internal_set_local_hardware_id(int32_t value) {
  
  _impl_.local_hardware_id_ = value;
}
inline void CpuTopologyProto_CpuDevice::set_local_hardware_id(int32_t value) {
  _internal_set_local_hardware_id(value);
  // @@protoc_insertion_point(field_set:xla.CpuTopologyProto.CpuDevice.local_hardware_id)
}

// -------------------------------------------------------------------

// CpuTopologyProto

// repeated .xla.CpuTopologyProto.CpuDevice cpu_devices = 1;
inline int CpuTopologyProto::_internal_cpu_devices_size() const {
  return _impl_.cpu_devices_.size();
}
inline int CpuTopologyProto::cpu_devices_size() const {
  return _internal_cpu_devices_size();
}
inline void CpuTopologyProto::clear_cpu_devices() {
  _impl_.cpu_devices_.Clear();
}
inline ::xla::CpuTopologyProto_CpuDevice* CpuTopologyProto::mutable_cpu_devices(int index) {
  // @@protoc_insertion_point(field_mutable:xla.CpuTopologyProto.cpu_devices)
  return _impl_.cpu_devices_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::CpuTopologyProto_CpuDevice >*
CpuTopologyProto::mutable_cpu_devices() {
  // @@protoc_insertion_point(field_mutable_list:xla.CpuTopologyProto.cpu_devices)
  return &_impl_.cpu_devices_;
}
inline const ::xla::CpuTopologyProto_CpuDevice& CpuTopologyProto::_internal_cpu_devices(int index) const {
  return _impl_.cpu_devices_.Get(index);
}
inline const ::xla::CpuTopologyProto_CpuDevice& CpuTopologyProto::cpu_devices(int index) const {
  // @@protoc_insertion_point(field_get:xla.CpuTopologyProto.cpu_devices)
  return _internal_cpu_devices(index);
}
inline ::xla::CpuTopologyProto_CpuDevice* CpuTopologyProto::_internal_add_cpu_devices() {
  return _impl_.cpu_devices_.Add();
}
inline ::xla::CpuTopologyProto_CpuDevice* CpuTopologyProto::add_cpu_devices() {
  ::xla::CpuTopologyProto_CpuDevice* _add = _internal_add_cpu_devices();
  // @@protoc_insertion_point(field_add:xla.CpuTopologyProto.cpu_devices)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::CpuTopologyProto_CpuDevice >&
CpuTopologyProto::cpu_devices() const {
  // @@protoc_insertion_point(field_list:xla.CpuTopologyProto.cpu_devices)
  return _impl_.cpu_devices_;
}

// repeated string machine_attributes = 4;
inline int CpuTopologyProto::_internal_machine_attributes_size() const {
  return _impl_.machine_attributes_.size();
}
inline int CpuTopologyProto::machine_attributes_size() const {
  return _internal_machine_attributes_size();
}
inline void CpuTopologyProto::clear_machine_attributes() {
  _impl_.machine_attributes_.Clear();
}
inline std::string* CpuTopologyProto::add_machine_attributes() {
  std::string* _s = _internal_add_machine_attributes();
  // @@protoc_insertion_point(field_add_mutable:xla.CpuTopologyProto.machine_attributes)
  return _s;
}
inline const std::string& CpuTopologyProto::_internal_machine_attributes(int index) const {
  return _impl_.machine_attributes_.Get(index);
}
inline const std::string& CpuTopologyProto::machine_attributes(int index) const {
  // @@protoc_insertion_point(field_get:xla.CpuTopologyProto.machine_attributes)
  return _internal_machine_attributes(index);
}
inline std::string* CpuTopologyProto::mutable_machine_attributes(int index) {
  // @@protoc_insertion_point(field_mutable:xla.CpuTopologyProto.machine_attributes)
  return _impl_.machine_attributes_.Mutable(index);
}
inline void CpuTopologyProto::set_machine_attributes(int index, const std::string& value) {
  _impl_.machine_attributes_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set:xla.CpuTopologyProto.machine_attributes)
}
inline void CpuTopologyProto::set_machine_attributes(int index, std::string&& value) {
  _impl_.machine_attributes_.Mutable(index)->assign(std::move(value));
  // @@protoc_insertion_point(field_set:xla.CpuTopologyProto.machine_attributes)
}
inline void CpuTopologyProto::set_machine_attributes(int index, const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  _impl_.machine_attributes_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set_char:xla.CpuTopologyProto.machine_attributes)
}
inline void CpuTopologyProto::set_machine_attributes(int index, const char* value, size_t size) {
  _impl_.machine_attributes_.Mutable(index)->assign(
    reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:xla.CpuTopologyProto.machine_attributes)
}
inline std::string* CpuTopologyProto::_internal_add_machine_attributes() {
  return _impl_.machine_attributes_.Add();
}
inline void CpuTopologyProto::add_machine_attributes(const std::string& value) {
  _impl_.machine_attributes_.Add()->assign(value);
  // @@protoc_insertion_point(field_add:xla.CpuTopologyProto.machine_attributes)
}
inline void CpuTopologyProto::add_machine_attributes(std::string&& value) {
  _impl_.machine_attributes_.Add(std::move(value));
  // @@protoc_insertion_point(field_add:xla.CpuTopologyProto.machine_attributes)
}
inline void CpuTopologyProto::add_machine_attributes(const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  _impl_.machine_attributes_.Add()->assign(value);
  // @@protoc_insertion_point(field_add_char:xla.CpuTopologyProto.machine_attributes)
}
inline void CpuTopologyProto::add_machine_attributes(const char* value, size_t size) {
  _impl_.machine_attributes_.Add()->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_add_pointer:xla.CpuTopologyProto.machine_attributes)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>&
CpuTopologyProto::machine_attributes() const {
  // @@protoc_insertion_point(field_list:xla.CpuTopologyProto.machine_attributes)
  return _impl_.machine_attributes_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>*
CpuTopologyProto::mutable_machine_attributes() {
  // @@protoc_insertion_point(field_mutable_list:xla.CpuTopologyProto.machine_attributes)
  return &_impl_.machine_attributes_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace xla

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_xla_2fpjrt_2fcpu_2fcpu_5ftopology_2eproto
