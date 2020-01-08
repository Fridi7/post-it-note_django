    $(document).ready(function(){

      $('#sort').change(function() {
        $.ajax({
          type: 'POST',
          url: 'notes/filters/',
          data: {
            "sort": $('#sort').val(),
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
          },
          success: filtersuccess,
        });
      });

      $('#filter').change(function() {
        $.ajax({
          type: 'POST',
          url: 'notes/filters/',
          data: {
            "filter": $('#filter').val(),
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
          },
          success: filtersuccess,
        });
      });

      $('#query').keyup(function(){
        $.ajax({
          type: 'POST',
          url: 'notes/filters/',
          data: {
            "query": $('#query').val(),
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
          },
          success: filtersuccess,
        });
      });

      function filtersuccess(data){
            console.log("success");
            $('#list').html(data);
      };

    });
