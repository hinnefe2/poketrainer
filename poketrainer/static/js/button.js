$('.add-mon').click(function () {
        $.ajax({
            url: '/api/team/'.concat($(this).attr("uid")),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

$('.drop-mon').click(function () {
        $.ajax({
            url: '/api/team/'.concat($(this).attr("uid")),
            type: 'DELETE',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

$('.sync-steps').click(function () {
        $.ajax({
            url: '/api/syncs/steps',
            type: 'POST',
            success: function(response) {
                alert(response);
            },
            error: function(error) {
                alert(error);
            }
        });
    });
