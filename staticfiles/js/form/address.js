$(function() {
    var address = [{
        country: 'Country',
        region: 'Region',
        regionArea: 'RegionArea',
        locality: 'Locality',
        localityName: 'LocalityName',
        street: 'Street',
        streetName: 'StreetName',
        house:'House',
        apartment:'Apartment'
    },{
        street: 'LiveStreet',
        streetName: 'LiveStreetName',
        house:'LiveHouse',
        apartment:'LiveApartment'

    },{
        country: 'EduCountry',
        region: 'EduRegion',
        regionArea: 'EduRegionArea',
        locality: 'EduLocality',
        localityName: 'EduLocalityName'
    }]


    var country_string=[];
    for (i in address) country_string.push('#'+address[i].country);
    $( country_string.join(', ') ).on('change', function(){
        for (var i in address){
            if ( address[i].country == this.id ){
                if(this.value == 10) {
                    $( '#'+address[i].region ).attr( 'disabled', false ).trigger('refresh');
                } else {
                    $( '#' + address[i].region         ).attr('disabled', true ).val('').trigger('refresh');
                    $( '#' + address[i].regionArea     ).attr('disabled', true ).empty().trigger('refresh');
                    $( '#' + address[i].localityName   ).attr('disabled', true ).val('');
                    $( '#' + address[i].streetName     ).attr('disabled', true ).val('');
                    $( '#' + address[i].house          ).attr('disabled', true ).val('');
                    $( '#' + address[i].apartment      ).attr('disabled', true ).val('');
                }
                break
            }
        }
    });

    var region_string=[];
    for (var i=0; i<address.length; i++) region_string.push('#'+address[i].region);
    $( region_string.join(', ') ).on('change', function(){
        for (var i=0; i<address.length; i++){
            if ( address[i].region == this.id ){
                var area = $( '#' + address[i].regionArea );
                if ( this.value != '' ){
                    area.attr('disabled', false).empty();
                    $.ajax({
                        type: "GET",
                        url: "/data/?task=loadregionareas&regionid="+this.value,
                        dataType: "json"
                    }).done(function( msg ) {
                        area.json2html({'id':0, 'name':'Нет района'}, {'tag':'option', 'value': '${id}', 'html': '${name}'});
                        area.json2html(msg,{'tag':'option', 'value': '${id}', 'html': '${name}'});
                        area.trigger('refresh');
                    });
                    $( '#' + address[i].localityName ).autocomplete( "option", "source", '/data/?task=loadlocalities&areaid=0' +
                        '&regionid='+$('#'+address[i].region).val() ).attr('disabled', false ).val('');

                } else {
                    area.empty();
                    $( '#' + address[i].regionArea   ).attr('disabled', true ).val('');
                    area.trigger('refresh');
                    $( '#' + address[i].localityName ).autocomplete( "option", "source", '/data/?task=loadlocalities&areaid=0' +
                        +'&regionid=0').attr('disabled', true ).val('');
                }
                $( '#' + address[i].streetName   ).attr('disabled', true ).val('');
                $( '#' + address[i].house        ).attr('disabled', true ).val('');
                $( '#' + address[i].apartment    ).attr('disabled', true ).val('');
                break
            }
        }
    })




    var area_string=[];
    for (var i=0; i<address.length; i++) area_string.push('#'+address[i].regionArea);
    $( area_string.join(', ') ).on('change', function(){
        for (var i=0; i<address.length; i++){
            if ( address[i].regionArea == this.id ){
                if ( this.value != '' ){
                    $( '#'+address[i].localityName ).autocomplete( "option", "source", '/data/?task=loadlocalities&regionid='+$('#'+address[i].region).val()+'&areaid='+this.value ).attr('disabled', false ).val('');
                    $( '#'+address[i].streetName   ).autocomplete( "option", "source", '/data/?task=loadstreets&areaid=0&localid=0').attr('disabled', true );
                    $( '#'+address[i].house        ).attr('disabled', true ).val('');
                    $( '#'+address[i].apartment    ).attr('disabled', true ).val('');
                } else {
                    $( '#'+address[i].localityName ).autocomplete( "option", "source", '/data/?task=loadlocalities&regionid='+$('#'+address[i].region).val()+'&areaid='+this.value ).attr('disabled', false ).val('');
                    $( '#'+address[i].streetName   ).autocomplete( "option", "source", "/data/?task=loadstreets&regionid=0&localid=0").attr('disabled', true ).val('');
                    $( '#'+address[i].street       ).val('');
                    $( '#'+address[i].house        ).attr('disabled', true ).val('');
                    $( '#'+address[i].apartment    ).attr('disabled', true ).val('');
                }
                break
            }
        }
    })



    local_string=[]
    for (i in address) local_string.push('#'+address[i].locality)
    $( local_string.join(', ') ).on('change', function(){
        for (i in address){
            if ( address[i].locality == this.id ){
                if ( this.value != '' ){
                    $( '#' + address[i].streetName ).autocomplete( "option", "source", "/data/?task=loadstreets&regionid="+$('#'+address[i].region).val()+'&localid='+$('#'+address[i].locality).val()).attr('disabled', false )

                    $( '#' + address[i].house     ).attr('disabled', false ).val('')
                    $( '#' + address[i].apartment ).attr('disabled', false ).val('')
                } else {

                    $( '#' + address[i].streetName ).autocomplete( "option", "source", "/data/?task=loadstreets&regionid=0&localid=0").attr('disabled', true ).val('')
                    $( '#' + address[i].street ).val('')

                    $( '#' + address[i].house     ).attr('disabled', true ).val('')
                    $( '#' + address[i].apartment ).attr('disabled', true ).val('')
                }
                break
            }
        }
    })










    $( "#LocalityName" ).autocomplete({
        minLength:3,
        source: '/data/?task=loadlocalities&areaid='+$('#RegionArea').val()+'&regionid='+$('#Region').val(),
        focus: function( event, ui ) {
            $( "#LocalityName" ).val( ui.item.name )
            return false
        },
        select: function( event, ui ) {
            $( "#LocalityName" ).val( ui.item.name )
            $( "#Locality" ).val( ui.item.id ).change()
            return false
        },
        change: function( event, ui ) {
            if(!ui.item){
                $( this ).val( "" )
                $( "#Locality" ).val( "" ).change()
                return false
            }
        }
    });

    $( "#LiveLocalityName" ).autocomplete({
        minLength:3,
        source: "/data/?task=loadlocalities&regionid="+$('#LiveRegion').val(),
        focus: function( event, ui ) {
            $( "#LiveLocalityName" ).val( ui.item.name )
            return false
        },
        select: function( event, ui ) {
            $( "#LiveLocalityName" ).val( ui.item.name )
            $( "#LiveLocality" ).val( ui.item.id ).change()
            return false
        },
        change: function( event, ui ) {
            if(!ui.item){
                $( this ).val( "" )
                $( "#LiveLocality" ).val( "" ).change()
                return false
            }
        }
    });


    $( "#EduLocalityName" ).autocomplete({
        minLength:3,
        source: "/data/?task=loadlocalities&regionid="+$('#EduRegion').val(),
        focus: function( event, ui ) {
            $( "#EduLocalityName" ).val( ui.item.name )
            return false
        },
        select: function( event, ui ) {
            $( "#EduLocalityName" ).val( ui.item.name )
            $( "#EduLocality" ).val( ui.item.id ).change()
            return false
        },
        change: function( event, ui ) {
            if(!ui.item){
                $( this ).val( "" )
                $( "#EduLocality" ).val( "" ).change()
                return false
            }
        }
    });

    $( "#prp" ).on('change', function(){
        if(this.checked == true)
            $('#prp-block').css('display','none');
        else
            $('#prp-block').css('display','');
    });




    $( "#StreetName" ).autocomplete({
        minLength:1,
        source: "/data/?task=loadstreets&regionid="+$('#Region').val()+'&localid='+$('#Locality').val(),
        focus: function( event, ui ) {
            $( "#StreetName" ).val( ui.item.name )
            return false
        },
        select: function( event, ui ) {
            $( "#StreetName" ).val( ui.item.name )
            console.log(ui.item.id)
            $( "#Street" ).val( ui.item.id ).change()
            return false
        },
        change: function( event, ui ) {
            if(!ui.item){
                $( this ).val( "" )
                $( "#Street" ).val( "" ).change()
                return false
            }
        }
    });


    $( "#LiveStreetName" ).autocomplete({
        minLength:3,
        source: '/data/?task=loadstreets&regionid=73&localid='+$('#LiveLocality').val(),
        focus: function( event, ui ) {
            $( "#LiveStreetName" ).val( ui.item.name )
            return false
        },
        select: function( event, ui ) {
            $( "#LiveStreetName" ).val( ui.item.name )
            console.log(ui.item.icon)
            $( "#LiveStreet" ).val( ui.item.id ).change()
            return false
        },
        change: function( event, ui ) {
            if(!ui.item){
                $( this ).val( "" )
                $( "#LiveStreet" ).val( "" ).change()
                return false
            }
        }
    });
});