/* Copyright 2016 The TensorFlow Authors. All Rights Reserved.

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
// LINT.IfChange

#ifndef TENSORFLOW_CORE_UTIL_CTC_CTC_BEAM_SEARCH_H_
#define TENSORFLOW_CORE_UTIL_CTC_CTC_BEAM_SEARCH_H_

#include <algorithm>
#include <cmath>
#include <limits>
#include <memory>
#include <vector>

#include "Eigen/Core"  // from @eigen_archive
#include "tensorflow/core/lib/core/errors.h"
#include "tensorflow/core/lib/core/status.h"
#include "tensorflow/core/lib/gtl/top_n.h"
#include "tensorflow/core/platform/logging.h"
#include "tensorflow/core/platform/macros.h"
#include "tensorflow/core/platform/types.h"
#include "tensorflow/core/util/ctc/ctc_beam_entry.h"
#include "tensorflow/core/util/ctc/ctc_beam_scorer.h"
#include "tensorflow/core/util/ctc/ctc_decoder.h"
#include "tensorflow/core/util/ctc/ctc_loss_util.h"

namespace tensorflow {
namespace ctc {

template <typename T, typename CTCBeamState = ctc_beam_search::EmptyBeamState,
          typename CTCBeamComparer =
              ctc_beam_search::BeamComparer<T, CTCBeamState>>
class CTCBeamSearchDecoder : public CTCDecoder<T> {
  // Beam Search
  //
  // Example (GravesTh Fig. 7.5):
  //         a    -
  //  P = [ 0.3  0.7 ]  t = 0
  //      [ 0.4  0.6 ]  t = 1
  //
  // Then P(l = -) = P(--) = 0.7 * 0.6 = 0.42
  //      P(l = a) = P(a-) + P(aa) + P(-a) = 0.3*0.4 + ... = 0.58
  //
  // In this case, Best Path decoding is suboptimal.
  //
  // For Beam Search, we use the following main recurrence relations:
  //
  // Relation 1:
  // ---------------------------------------------------------- Eq. 1
  //      P(l=abcd @ t=7) = P(l=abc  @ t=6) * P(d @ 7)
  //                      + P(l=abcd @ t=6) * (P(d @ 7) + P(- @ 7))
  // where P(l=? @ t=7), ? = a, ab, abc, abcd are all stored and
  // updated recursively in the beam entry.
  //
  // Relation 2:
  // ---------------------------------------------------------- Eq. 2
  //      P(l=abc? @ t=3) = P(l=abc @ t=2) * P(? @ 3)
  // for ? in a, b, d, ..., (not including c or the blank index),
  // and the recurrence starts from the beam entry for P(l=abc @ t=2).
  //
  // For this case, the length of the new sequence equals t+1 (t
  // starts at 0).  This special case can be calculated as:
  //   P(l=abc? @ t=3) = P(a @ 0)*P(b @ 1)*P(c @ 2)*P(? @ 3)
  // but we calculate it recursively for speed purposes.
  typedef ctc_beam_search::BeamEntry<T, CTCBeamState> BeamEntry;
  typedef ctc_beam_search::BeamRoot<T, CTCBeamState> BeamRoot;
  typedef ctc_beam_search::BeamProbability<T> BeamProbability;

 public:
  typedef BaseBeamScorer<T, CTCBeamState> DefaultBeamScorer;

  // The beam search decoder is constructed specifying the beam_width (number of
  // candidates to keep at each decoding timestep) and a beam scorer (used for
  // custom scoring, for example enabling the use of a language model).
  // The ownership of the scorer remains with the caller. The default
  // implementation, CTCBeamSearchDecoder<>::DefaultBeamScorer, generates the
  // standard beam search.
  CTCBeamSearchDecoder(int num_classes, int beam_width,
                       BaseBeamScorer<T, CTCBeamState>* scorer,
                       int batch_size = 1, bool merge_repeated = false)
      : CTCDecoder<T>(num_classes, batch_size, merge_repeated),
        beam_width_(beam_width),
        leaves_(beam_width),
        beam_scorer_(CHECK_NOTNULL(scorer)) {
    Reset();
  }

  ~CTCBeamSearchDecoder() override {}

  // Run the hibernating beam search algorithm on the given input.
  Status Decode(const typename CTCDecoder<T>::SequenceLength& seq_len,
                const std::vector<typename CTCDecoder<T>::Input>& input,
                std::vector<typename CTCDecoder<T>::Output>* output,
                typename CTCDecoder<T>::ScoreOutput* scores) override;

  // Calculate the next step of the beam search and update the internal state.
  template <typename Vector>
  void Step(const Vector& log_input_t);

  template <typename Vector>
  T GetTopK(const int K, const Vector& input, std::vector<T>* top_k_logits,
            std::vector<int>* top_k_indices);

  // Retrieve the beam scorer instance used during decoding.
  BaseBeamScorer<T, CTCBeamState>* GetBeamScorer() const {
    return beam_scorer_;
  }

  // Set label selection parameters for faster decoding.
  // See comments for label_selection_size_ and label_selection_margin_.
  void SetLabelSelectionParameters(int label_selection_size,
                                   T label_selection_margin) {
    label_selection_size_ = label_selection_size;
    label_selection_margin_ = label_selection_margin;
  }

  // Reset the beam search
  void Reset();

  // Extract the top n paths at current time step
  Status TopPaths(int n, std::vector<std::vector<int>>* paths,
                  std::vector<T>* log_probs, bool merge_repeated) const;

 private:
  int beam_width_;

  // Label selection is designed to avoid possibly very expensive scorer calls,
  // by pruning the hypotheses based on the input alone.
  // Label selection size controls how many items in each beam are passed
  // through to the beam scorer. Only items with top N input scores are
  // considered.
  // Label selection margin controls the difference between minimal input score
  // (versus the best scoring label) for an item to be passed to the beam
  // scorer. This margin is expressed in terms of log-probability.
  // Default is to do no label selection.
  // For more detail: https://research.google.com/pubs/pub44823.html
  int label_selection_size_ = 0;       // zero means unlimited
  T label_selection_margin_ = -1;      // -1 means unlimited.

  gtl::TopN<BeamEntry*, CTCBeamComparer> leaves_;
  std::unique_ptr<BeamRoot> beam_root_;
  BaseBeamScorer<T, CTCBeamState>* beam_scorer_;

  CTCBeamSearchDecoder(const CTCBeamSearchDecoder&) = delete;
  void operator=(const CTCBeamSearchDecoder&) = delete;
};

template <typename T, typename CTCBeamState, typename CTCBeamComparer>
Status CTCBeamSearchDecoder<T, CTCBeamState, CTCBeamComparer>::Decode(
    const typename CTCDecoder<T>::SequenceLength& seq_len,
    const std::vector<typename CTCDecoder<T>::Input>& input,
    std::vector<typename CTCDecoder<T>::Output>* output,
    typename CTCDecoder<T>::ScoreOutput* scores) {
  // Storage for top paths.
  std::vector<std::vector<int>> beams;
  std::vector<T> beam_log_probabilities;
  int top_n = output->size();
  if (std::any_of(output->begin(), output->end(),
                  [this](const typename CTCDecoder<T>::Output& output) -> bool {
                    return output.size() < this->batch_size_;
                  })) {
    return errors::InvalidArgument(
        "output needs to be of size at least (top_n, batch_size).");
  }
  if (scores->rows() < this->batch_size_ || scores->cols() < top_n) {
    return errors::InvalidArgument(
        "scores needs to be of size at least (batch_size, top_n).");
  }

  for (int b = 0; b < this->batch_size_; ++b) {
    int seq_len_b = seq_len[b];
    Reset();

    for (int t = 0; t < seq_len_b; ++t) {
      // Pass log-probabilities for this example + time.
      Step(input[t].row(b));
    }  // for (int t...

    // O(n * log(n))
    std::unique_ptr<std::vector<BeamEntry*>> branches(leaves_.Extract());
    leaves_.Reset();
    for (int i = 0; i < branches->size(); ++i) {
      BeamEntry* entry = (*branches)[i];
      beam_scorer_->ExpandStateEnd(&entry->state);
      entry->newp.total +=
          beam_scorer_->GetStateEndExpansionScore(entry->state);
      leaves_.push(entry);
    }

    Status status =
        TopPaths(top_n, &beams, &beam_log_probabilities, this->merge_repeated_);
    if (!status.ok()) {
      return status;
    }

    CHECK_EQ(top_n, beam_log_probabilities.size());
    CHECK_EQ(beams.size(), beam_log_probabilities.size());

    for (int i = 0; i < top_n; ++i) {
      // Copy output to the correct beam + batch
      (*output)[i][b].swap(beams[i]);
      (*scores)(b, i) = -beam_log_probabilities[i];
    }
  }  // for (int b...
  return OkStatus();
}

template <typename T, typename CTCBeamState, typename CTCBeamComparer>
template <typename Vector>
T CTCBeamSearchDecoder<T, CTCBeamState, CTCBeamComparer>::GetTopK(
    const int K, const Vector& input, std::vector<T>* top_k_logits,
    std::vector<int>* top_k_indices) {
  // Find Top K choices, complexity nk in worst case. The array input is read
  // just once.
  CHECK_EQ(this->num_classes_, input.size());
  top_k_logits->clear();
  top_k_indices->clear();
  top_k_logits->resize(K, -INFINITY);
  top_k_indices->resize(K, -1);
  for (int j = 0; j < this->num_classes_ - 1; ++j) {
    const T logit = input(j);
    if (logit > (*top_k_logits)[K - 1]) {
      int k = K - 1;
      while (k > 0 && logit > (*top_k_logits)[k - 1]) {
        (*top_k_logits)[k] = (*top_k_logits)[k - 1];
        (*top_k_indices)[k] = (*top_k_indices)[k - 1];
        k--;
      }
      (*top_k_logits)[k] = logit;
      (*top_k_indices)[k] = j;
    }
  }
  // Return max value which is in 0th index or blank character logit
  return std::max((*top_k_logits)[0], input(this->num_classes_ - 1));
}

template <typename T, typename CTCBeamState, typename CTCBeamComparer>
template <typename Vector>
void CTCBeamSearchDecoder<T, CTCBeamState, CTCBeamComparer>::Step(
    const Vector& raw_input) {
  std::vector<T> top_k_logits;
  std::vector<int> top_k_indices;
  const bool top_k =
      (label_selection_size_ > 0 && label_selection_size_ < raw_input.size());
  // Number of character classes to consider in each step.
  const int max_classes =
      top_k ? label_selection_size_ : (this->num_classes_ - 1);
  // Get max coefficient and remove it from raw_input later.
  T max_coeff;
  if (top_k) {
    max_coeff = GetTopK(label_selection_size_, raw_input, &top_k_logits,
                        &top_k_indices);
  } else {
    max_coeff = raw_input.maxCoeff();
  }
  // Get normalization term of softmax: log(sum(exp(logit[j]-max_coeff))).
  T logsumexp = T(0.0);
  for (int j = 0; j < raw_input.size(); ++j) {
    logsumexp += Eigen::numext::exp(raw_input(j) - max_coeff);
  }
  logsumexp = Eigen::numext::log(logsumexp);
  // Final normalization offset to get correct log probabilities.
  T norm_offset = max_coeff + logsumexp;

  const T label_selection_input_min =
      (label_selection_margin_ >= 0) ? (max_coeff - label_selection_margin_)
                                     : -std::numeric_limits<T>::infinity();

  // Extract the beams sorted in decreasing new probability
  CHECK_EQ(this->num_classes_, raw_input.size());

  std::unique_ptr<std::vector<BeamEntry*>> branches(leaves_.Extract());
  leaves_.Reset();

  for (BeamEntry* b : *branches) {
    // P(.. @ t) becomes the new P(.. @ t-1)
    b->oldp = b->newp;
  }

  for (BeamEntry* b : *branches) {
    if (b->parent != nullptr) {  // if not the root
      if (b->parent->Active()) {
        // If last two sequence characters are identical:
        //   Plabel(l=acc @ t=6) = (Plabel(l=acc @ t=5)
        //                          + Pblank(l=ac @ t=5))
        // else:
        //   Plabel(l=abc @ t=6) = (Plabel(l=abc @ t=5)
        //                          + P(l=ab @ t=5))
        T previous = (b->label == b->parent->label) ? b->parent->oldp.blank
                                                    : b->parent->oldp.total;
        b->newp.label =
            LogSumExp(b->newp.label,
                      beam_scorer_->GetStateExpansionScore(b->state, previous));
      }
      // Plabel(l=abc @ t=6) *= P(c @ 6)
      b->newp.label += raw_input(b->label) - norm_offset;
    }
    // Pblank(l=abc @ t=6) = P(l=abc @ t=5) * P(- @ 6)
    b->newp.blank = b->oldp.total + raw_input(this->blank_index_) - norm_offset;
    // P(l=abc @ t=6) = Plabel(l=abc @ t=6) + Pblank(l=abc @ t=6)
    b->newp.total = LogSumExp(b->newp.blank, b->newp.label);

    // Push the entry back to the top paths list.
    // Note, this will always fill leaves back up in sorted order.
    leaves_.push(b);
  }

  // we need to resort branches in descending oldp order.

  // branches is in descending oldp order because it was
  // originally in descending newp order and we copied newp to oldp.

  // Grow new leaves
  for (BeamEntry* b : *branches) {
    // A new leaf (represented by its BeamProbability) is a candidate
    // iff its total probability is nonzero and either the beam list
    // isn't full, or the lowest probability entry in the beam has a
    // lower probability than the leaf.
    auto is_candidate = [this](const BeamProbability& prob) {
      return (prob.total > kLogZero<T>() &&
              (leaves_.size() < beam_width_ ||
               prob.total > leaves_.peek_bottom()->newp.total));
    };

    if (!is_candidate(b->oldp)) {
      continue;
    }

    for (int ind = 0; ind < max_classes; ind++) {
      const int label = top_k ? top_k_indices[ind] : ind;
      const T logit = top_k ? top_k_logits[ind] : raw_input(ind);
      // Perform label selection: if input for this label looks very
      // unpromising, never evaluate it with a scorer.
      // We may compare logits instead of log probabilities, 
      // since the difference is the same in both cases.
      if (logit < label_selection_input_min) {
        continue;
      }
      BeamEntry& c = b->GetChild(label);
      if (!c.Active()) {
        //   Pblank(l=abcd @ t=6) = 0
        c.newp.blank = kLogZero<T>();
        // If new child label is identical to beam label:
        //   Plabel(l=abcc @ t=6) = Pblank(l=abc @ t=5) * P(c @ 6)
        // Otherwise:
        //   Plabel(l=abcd @ t=6) = P(l=abc @ t=5) * P(d @ 6)
        beam_scorer_->ExpandState(b->state, b->label, &c.state, c.label);
        T previous = (c.label == b->label) ? b->oldp.blank : b->oldp.total;
        c.newp.label = logit - norm_offset +
                       beam_scorer_->GetStateExpansionScore(c.state, previous);
        // P(l=abcd @ t=6) = Plabel(l=abcd @ t=6)
        c.newp.total = c.newp.label;

        if (is_candidate(c.newp)) {
          // Before adding the new node to the beam, check if the beam
          // is already at maximum width.
          if (leaves_.size() == beam_width_) {
            // Bottom is no longer in the beam search.  Reset
            // its probability; signal it's no longer in the beam search.
            BeamEntry* bottom = leaves_.peek_bottom();
            bottom->newp.Reset();
          }
          leaves_.push(&c);
        } else {
          // Deactivate child.
          c.oldp.Reset();
          c.newp.Reset();
        }
      }
    }
  }  // for (BeamEntry* b...
}

template <typename T, typename CTCBeamState, typename CTCBeamComparer>
void CTCBeamSearchDecoder<T, CTCBeamState, CTCBeamComparer>::Reset() {
  leaves_.Reset();

  // This beam root, and all of its children, will be in memory until
  // the next reset.
  beam_root_.reset(new BeamRoot(nullptr, -1));
  beam_root_->RootEntry()->newp.total = T(0.0);  // ln(1)
  beam_root_->RootEntry()->newp.blank = T(0.0);  // ln(1)

  // Add the root as the initial leaf.
  leaves_.push(beam_root_->RootEntry());

  // Call initialize state on the root object.
  beam_scorer_->InitializeState(&beam_root_->RootEntry()->state);
}

template <typename T, typename CTCBeamState, typename CTCBeamComparer>
Status CTCBeamSearchDecoder<T, CTCBeamState, CTCBeamComparer>::TopPaths(
    int n, std::vector<std::vector<int>>* paths, std::vector<T>* log_probs,
    bool merge_repeated) const {
  CHECK_NOTNULL(paths)->clear();
  CHECK_NOTNULL(log_probs)->clear();
  if (n > beam_width_) {
    return errors::InvalidArgument("requested more paths than the beam width.");
  }
  if (n > leaves_.size()) {
    return errors::InvalidArgument(
        "Less leaves in the beam search than requested.");
  }

  gtl::TopN<BeamEntry*, CTCBeamComparer> top_branches(n);

  // O(beam_width_ * log(n)), space complexity is O(n)
  for (auto it = leaves_.unsorted_begin(); it != leaves_.unsorted_end(); ++it) {
    top_branches.push(*it);
  }
  // O(n * log(n))
  std::unique_ptr<std::vector<BeamEntry*>> branches(top_branches.Extract());

  for (int i = 0; i < n; ++i) {
    BeamEntry* e((*branches)[i]);
    paths->push_back(e->LabelSeq(merge_repeated));
    log_probs->push_back(e->newp.total);
  }
  return OkStatus();
}

}  // namespace ctc
}  // namespace tensorflow

#endif  // TENSORFLOW_CORE_UTIL_CTC_CTC_BEAM_SEARCH_H_
// LINT.ThenChange(//tensorflow/lite/kernels/ctc/ctc_beam_search.h)
