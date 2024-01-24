from classifier.zsc import ZSC
import pandas as pd
import os


ex_template = {
    "k": 5,
    "model": "all-MiniLM-L12-v2",
    "lower_case": True,
    "embedding": "sentence",
    "cs": "CoClass",
    "dimension": "Tillgångssystem",
    "lang": "en",
    "hierarchy": "bottomup",
    #'doubletap': False,
    "cutoff": 0.30,
}

x = ZSC(ex_template)


# user input
os.system("cls||clear")

print("-------------------------\n")
print("Welcome to MiCRA!\n")
print("You can exit at anytime by typing 'exit' or presing ctrl-c\n")
print("-------------------------")
print("How many labels per requirement do you want the tool to recommender?")

k = int(input())

ex_template["k"] = k

user_input = ""
while user_input != "exit":
    print("-------------------------\n")
    print("Please enter the text that you want to classify:\n")

    user_input = str(input())

    requirements = {
        "all_text": [user_input],
        "all_text_clean": ["-"],
    }
    data = pd.DataFrame(requirements)

    # classify
    result, elapsed_time = x.classify(data)

    # print results
    single_result = {
        "predicted_labels": result["predicted_labels"][0],
        "predicted_labells_desc": result["predicted_labels_names"][0],
        "scores": result["scores"][0],
    }

    result_df = pd.DataFrame(single_result)
    print("\nClassification results:\n")
    print(result_df)
    print("\n")
    print(f"Elapsed time: {elapsed_time} s")


# for code, label, score in zip(result['predicted_labels'][0], result['predicted_labels_names'][0], result['scores'][0]):
#    print (f'{code} - {label} :' , '{:.2f}'.format(score))
