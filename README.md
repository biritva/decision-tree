# decision-tree
**My implementation of decision tree**

* 2 решающих класса: 
  DecisionTreeRegressor - дерево для регрессии.
  DecisionTreeClassifier - дерево для класификациию
* Параметры: 
  criterion('mse','mae', 'gini', 'entropy') - выбор критерия, два первых для регрессии, два вторых для энтропии;
  max_depth - глубина дерева ;
  min_samples - число семплов в листе.
