function onDeleteArticle() {
    response = confirm('This action will delete article');
    if (response == false){
        return false;
    } 
}