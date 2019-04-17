function addToElementsClass (tagName, className) {
  const elements = document.getElementsByTagName(tagName);
  for (var i=0; i<elements.length; i++){
    elements[i].className += className;
  };
};
