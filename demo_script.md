# 3-4 Minute Demo Script

## Opening

Good day. We are presenting our expert system prototype titled **Cognitive UX Design Auditor**.

The purpose of this system is to help beginner UI and UX designers detect cognitive usability issues in interface designs. The system focuses on problems such as high cognitive load, unclear visual hierarchy, inconsistent labels, weak error prevention, poor feedback, and confusing navigation.

## Expert System Components

Our prototype has three main expert system components.

First, the **Knowledge Base**.  
The knowledge base stores cognitive UX rules using IF-THEN logic. For example, if the number of visible options is more than seven and the options are not grouped, then the system detects a high cognitive load issue.

Second, the **Inference Engine**.  
The inference engine uses forward chaining. It starts from the facts given by the user in the audit form, checks those facts against the rules, and fires all matching rules.

Third, the **User Interface**.  
The user interface is built using Streamlit. It allows the user to answer questions about a screen design and then view the audit result.

## Demo Steps

For this demo, I will choose the **Overloaded dashboard** sample scenario.

In this case, the interface has many visible options, the options are not grouped, the primary action is not clear, labels are inconsistent, navigation is unclear, and the layout is crowded.

Now I click **Run UX Audit**.

The system produces the audit result. It shows the overall risk, severity score, and number of triggered rules.

The triggered issues include cognitive load, visual hierarchy, consistency, navigation clarity, and layout crowding.

Each result also includes an explanation. For example, the cognitive load rule is triggered because the interface has more than seven visible options and the options are not grouped.

The system also gives a recommendation. It suggests grouping related options, removing unnecessary choices, and simplifying the interface.

## Closing

This prototype is useful because it does not only give a pass or fail result. It explains which rule was triggered, why the issue matters, the severity level, and how the designer can improve the interface.

Therefore, our system works as an explainable expert assistant for early-stage cognitive UX auditing.
