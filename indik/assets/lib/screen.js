function fillThem(){
    $(".fill-parent").each(function(index, item){
        //get parent
        var el, parent, siblingsHeight = 0, parentHeight;
        el = $(item);
        parent = el.parent();
        parentHeight = parent.height();
        var s = el.prevAll().each(function(idx, itm){
               siblingsHeight += $(itm).height();
        });
        el.height(parentHeight - siblingsHeight);
        el.css('top', siblingsHeight);

    });
}

$(function(){

    
    $(window).resize(function() {
      fillThem();
    });
    fillThem();

});

