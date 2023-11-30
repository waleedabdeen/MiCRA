import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys


#visualize
def multi_label_heatmap(cmx, labels):
    total_figures = len(cmx)
    columns = 5 if total_figures >= 5 else total_figures
    rows = 2 if total_figures // 5 == 0 else total_figures // 5

    fig, ax = plt.subplots(rows, columns)
    fig.set_size_inches(20, 3 * rows)
    fig.tight_layout(pad=3)

    for i, (c, l) in enumerate(zip(cmx, labels)):
        row = i // columns
        column = i % columns
        sns.heatmap(c, annot=True, fmt="d", ax=ax[row, column], cmap=plt.cm.Blues)
        ax[row, column].set(
            ylabel="True",
            xlabel="Predicted",
            xticklabels=["0", "1"],
            yticklabels=["0", "1"],
            title=l,
        )
        ax[row, column].title.set_size(10)

    plt.show()


def get_predicted_cms(cms):
    # predicted => fp + tp != 0
    return cms[((cms[:, 0, 1] > 0) | (cms[:, 1, 1] > 0))]


def get_true_and_predicted_cms(cms):
    # predicted => fp + tp != 0
    # true => fn + tp != 0
    return cms[((cms[:, 0, 1] > 0) | (cms[:, 1, 1] > 0) | (cms[:, 1, 0] > 0))]


def get_true_cms(cms):
    # true => fn + tp != 0
    true_cms = cms[((cms[:, 1, 1] > 0) | (cms[:, 1, 0] > 0))]
    return true_cms


def f_beta(recall, precision, B):
    return (1 + pow(B, 2)) * recall * precision / (recall + (pow(B, 2) * precision))


def custom_evaluation(cms):
    tn = cms[:, 0, 0].sum()
    # micros
    all_fn = cms[:, 1, 0].sum()
    all_fp = cms[:, 0, 1].sum()
    all_tp = cms[:, 1, 1].sum()

    micro_recall = all_tp / (all_tp + all_fn)
    micro_precision = all_tp / (all_tp + all_fp)
    micro_f1 = f_beta(micro_recall, micro_precision, 1)
    micro_f2 = f_beta(micro_recall, micro_precision, 2)
    # macros
    all_recall = 0
    all_precision = 0

    for c in cms:
        min_value = sys.float_info.min
        tp = c[1, 1]
        fn = c[1, 0]
        fp = c[0, 1]
        recall_per_class = tp / (tp + fn + min_value)
        precision_per_class = tp / (tp + fp + min_value)

        all_recall += recall_per_class
        all_precision += precision_per_class

    macro_recall = all_recall / len(cms)
    macro_precision = all_precision / len(cms)
    macro_f1 = f_beta(macro_recall, macro_precision, 1)
    macro_f2 = f_beta(macro_recall, macro_precision, 2)

    result = {
        "micro_recall": micro_recall,
        "micro_precision": micro_precision,
        "micro_f1": micro_f1,
        "micro_f2": micro_f2,
        "macro_recall": macro_recall,
        "macro_precision": macro_precision,
        "macro_f1": macro_f1,
        "macro_f2": macro_f2,
    }
    return result


def calculate_subset_metrics(confusion_matrix):
    # all    
    all_labels_results = custom_evaluation(confusion_matrix)
    
    predicted_cms = get_predicted_cms(confusion_matrix)
    predicted_labels_results = custom_evaluation(predicted_cms)

    true_cms = get_true_cms(confusion_matrix)
    true_labels_results = custom_evaluation(true_cms)

    union_cms = get_true_and_predicted_cms(confusion_matrix)
    union_results = custom_evaluation(union_cms)

    return {
       'all':  all_labels_results,
       'predicted': predicted_labels_results,
       'true': true_labels_results,
       'union': union_results,
    }


def apk(y_true, y_pred, k_max=0):

  # Check if all elements in lists are unique
  if len(set(y_true)) != len(y_true):
    raise ValueError("Values in y_true are not unique")

  if len(set(y_pred)) != len(y_pred):
    raise ValueError("Values in y_pred are not unique")

  if k_max != 0:
    y_pred = y_pred[:k_max]

  correct_predictions = 0
  running_sum = 0

  for i, yp_item in enumerate(y_pred):
    
    k = i+1 # our rank starts at 1
    
    if yp_item in y_true:
      correct_predictions += 1
      running_sum += correct_predictions/k

  return running_sum/len(y_true)

def mapk(true_labels, predicted_labels, k=0):
  return np.mean([apk(a,p,k) for a,p in zip(true_labels, predicted_labels)])


def distance_evaluation(Y_labels, X_labels, max_distance):   
   distances = []
   for y, x in zip(Y_labels, X_labels):
      d = distance_between_labels_arrays(y, x, max_distance)
      if len(d) != 0:
        distances.append(d)

   mean = np.mean([np.mean(dis_list) for dis_list in distances])

   normalized_distances = normalize_distances(distances, max_distance)
   normalized_mean = np.mean([np.mean(dis_list) for dis_list in normalized_distances])
   
   return distances, mean, normalized_distances, normalized_mean


def normalize_distances(distances, max_distance):
   return [[d / max_distance for d in d_a] for d_a in distances]

   
def distance_between_labels_arrays(true_labels, predicted_labels, max_distance):
   result = []
   for l1 in true_labels:
      if len(predicted_labels) > 0:
        min_d = max_distance
        for l2 in predicted_labels:
          d = distance_between_labels(l1, l2)
          if d < min_d:
            min_d = d
            
        result.append(min_d)
   
   return result

def distance_between_labels(l1, l2):   
   l1_len = len(l1)   
   l2_len = len(l2)
   min_len = min(l1_len, l2_len)
   
   offset = 0
   for i in range(min_len):
      if l1[i] != l2[i]:
         offset = 0
         break
      else:
        offset = 1
         
   distance = l1_len + l2_len - ((i + offset) * 2)

   return distance


def max_depth_per_dimension(df_taxonomy, dimension):
   df_filtered = df_taxonomy[df_taxonomy['dimension'] == dimension]
   return int(df_filtered['identifier'].astype(bytes).str.len().max())

# cmx2 = [[[10,20],[2,0]], [[4,30],[10,2]], [[10,20],[2,0]], [[4,30],[10,2]]]
# labels = ['1', '1A', '1B', '1C']
# multi_label_heatmap(cmx2, labels)
