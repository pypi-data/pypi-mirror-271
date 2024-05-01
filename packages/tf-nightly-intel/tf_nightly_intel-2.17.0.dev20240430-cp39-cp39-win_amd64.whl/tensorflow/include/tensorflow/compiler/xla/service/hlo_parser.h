/* Copyright 2017 The OpenXLA Authors.

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

#ifndef XLA_SERVICE_HLO_PARSER_H_
#define XLA_SERVICE_HLO_PARSER_H_

#include <memory>
#include <vector>

#include "absl/strings/string_view.h"
#include "xla/hlo/ir/hlo_computation.h"
#include "xla/hlo/ir/hlo_instruction.h"
#include "xla/hlo/ir/hlo_module.h"
#include "xla/service/hlo_lexer.h"
#include "xla/statusor.h"
#include "xla/xla_data.pb.h"

namespace xla {

// Given a string in the HloModule::ToString() format, parses the string and
// creates a HloModule with the given config.
// Note: Tests derived from HloTestBase should use
// ParseAndReturnVerifiedModule() instead!
absl::StatusOr<std::unique_ptr<HloModule>> ParseAndReturnUnverifiedModule(
    absl::string_view str, const HloModuleConfig& config);

// Given a string in the HloModule::ToString() format, parses the string and
// creates a HloModule with default config.
// Note: Tests derived from HloTestBase should use
// ParseAndReturnVerifiedModule() instead!
absl::StatusOr<std::unique_ptr<HloModule>> ParseAndReturnUnverifiedModule(
    absl::string_view str);

// Parses sharding from str. str is supposed to contain the body of the
// sharding, i.e. just the rhs of the "sharding={...}" attribute string, e.g.,
// "{replicated}".
absl::StatusOr<HloSharding> ParseSharding(absl::string_view str);

// Parses frontend attributes from str. str is supposed to contain the body of
// the frontend attributes , i.e. just the rhs of the
// "frontend_attributes={...}" attribute string, e.g.,
// "{attr_a=a,attr_b=b}".
absl::StatusOr<FrontendAttributes> ParseFrontendAttributes(
    absl::string_view str);

// Parses statistics viz from str. str is supposed to contain the body of the
// statistics visualization, i.e. just the rhs of the "statistics={...}"
// attribute string, e.g., "{visualizing_index=1,nan_percent=50}".
absl::StatusOr<StatisticsViz> ParseStatisticsViz(absl::string_view str);

// Parses parameter replication from str. str is supposed to contain the body of
// the parameter replication, i.e. just the rhs of the
// "parameter_replication={...}" attribute string, e.g., "{true, false}".
absl::StatusOr<std::vector<bool>> ParseParameterReplication(
    absl::string_view str);

// Parses the result of window_util::ToString(const Window&).
absl::StatusOr<Window> ParseWindow(absl::string_view str);

// Parses the result of ConvolutionDimensionNumbersToString(), e.g.
// "b0f_0io->b0f".
absl::StatusOr<ConvolutionDimensionNumbers> ParseConvolutionDimensionNumbers(
    absl::string_view str);

// Parses the result of PaddingConfigToString(), e.g. "0_0x1_1".
absl::StatusOr<PaddingConfig> ParsePaddingConfig(absl::string_view str);

// Parses and returns a Shape::ToString-format string.
absl::StatusOr<Shape> ParseShape(absl::string_view str);

// Parses and returns a Layout::ToString-format string.
absl::StatusOr<Layout> ParseLayout(absl::string_view str);

// Parses and returns a std::vector<ReplicaGroup> from str. str is supposed to
// contain a list of the replica groups, i.e. just the rhs of the
// "replica_groups={...}" attribute string, e.g., "{{0,1}, {2,3}}".
absl::StatusOr<std::vector<ReplicaGroup>> ParseReplicaGroupsOnly(
    absl::string_view str);

class HloParser {
 public:
  // Runs the parser and constructs the resulting HLO in the given (empty)
  // HloModule. Returns the error status in case an error occurred.
  virtual Status Run(HloModule* module) = 0;
  virtual ~HloParser() {}

 private:
  static std::unique_ptr<HloParser> CreateHloParserForTests(
      absl::string_view str);
  friend class VerifiedHloModule;
};

}  // namespace xla

#endif  // XLA_SERVICE_HLO_PARSER_H_
