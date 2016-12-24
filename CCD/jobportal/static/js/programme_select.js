$("#leader_btech_bdes").change(function(){
    var status = this.checked;
    $('.btech_bdes').each(function(){
        this.checked = status;
    });
});

$('.btech_bdes').change(function(){
    if(this.checked == false){
        $("#leader_btech_bdes")[0].checked = false;
    }
});

$("#leader_minor").change(function(){
    var status = this.checked;
    $('.minor').each(function(){
        this.checked = status;
    });
});

$('.minor').change(function(){
    if(this.checked == false){
        $("#leader_minor")[0].checked = false;
    }
});

$("#leader_mtech_mdes").change(function(){
    var status = this.checked;
    $('.mtech_mdes').each(function(){
        this.checked = status;
    });
});

$('.mtech_mdes').change(function(){
    if(this.checked == false){
        $("#leader_mtech_mdes")[0].checked = false;
    }
});

$("#leader_msc").change(function(){
    var status = this.checked;
    $('.msc').each(function(){
        this.checked = status;
    });
});

$('.msc').change(function(){
    if(this.checked == false){
        $("#leader_msc")[0].checked = false;
    }
});

$("#leader_ma").change(function(){
    var status = this.checked;
    $('.ma').each(function(){
        this.checked = status;
    });
});

$('.ma').change(function(){
    if(this.checked == false){
        $("#leader_ma")[0].checked = false;
    }
});

$("#leader_phd").change(function(){
    var status = this.checked;
    $('.phd').each(function(){
        this.checked = status;
    });
});

$('.phd').change(function(){
    if(this.checked == false){
        $("#leader_phd")[0].checked = false;
    }
});

$("#leader_msr").change(function(){
    var status = this.checked;
    $('.msr').each(function(){
        this.checked = status;
    });
});

$('.msr').change(function(){
    if(this.checked == false){
        $("#leader_msr")[0].checked = false;
    }
});
