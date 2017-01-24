// JavaScript Document
jQuery(document).ready(function($) {

    if ($('div').hasClass('sidebarCinza')) {
        $( "#datepicker" ).datepicker();
        $( "#datepicker2" ).datepicker();
    }
  
    //CALCULA ALTURA SIDEBAR
    var alturaTela = 0;
    alturaTela = $(window).height();
    $('.divSidebar ul.menuNav').css('height',alturaTela - 114);
    
    
    $('.ativarEdicao').click(function () {
        $('.richText').slideToggle();
    });
    
    var srcImg = '';
    $('.listIcones ul li').click(function(){
        $('.listIcones ul li img').removeClass('active');
        $(this).find('img').toggleClass('active');
        srcImg = $(this).find('img').attr('src');
        $('.divPreview .icoPreview').attr('src',srcImg);
        $('.contentGeral .divPreview').show();
        return false;
    });
    
    var inputTitulo = '';
    $( ".formPainel .inputTitulo" ).on('keyup', function () {
        inputTitulo = $(this).val();
        $('.divPreview .changeh3').html(inputTitulo);
        $('.contentGeral .divPreview').show();
    });
    
    var inputTexto = '';
    $( ".formPainel .inputTexto" ).on('keyup', function () {
        inputTexto = $(this).val();
        $('.divPreview .changep').html(inputTexto);
        $('.contentGeral .divPreview').show();
    });
    
    
    var srcImg = '';
    var alternativo = '';
    var titleIco = '';
    $('.listIconesGrande ul li').click(function(){
        $('.listIconesGrande ul li img').removeClass('active');
        $(this).find('img').toggleClass('active');
        srcImg = $(this).find('img').attr('src');
        $('.sidebarCinza .imgSelect').attr('src',srcImg);
        alternativo = $(this).find('img').attr('alt');
        $('.divPublicacoes .sidebarCinza .inputAltGaleria').val(alternativo);
        titleIco = $(this).find('img').attr('title');
        $('.divPublicacoes .sidebarCinza .inputTitGaleria').val(titleIco);
        return false;
    });


    $('#paramConfiguracaoSPAgora .btnSalvar').click(function(event){
        event.preventDefault();
        var habilita;
        try{
            habilita = $("input[name='rdbHabilita']:checked").attr('value');
            if(!habilita){
                habilita = '';
            }
        }catch(err){
            habilita = '';
        }
        if(habilita.length > 0){
           site_url = $('.breadcrumb a').first().attr('href');
           url = site_url + '/@@habilitar-dashboard';
           $.post( url,
           {
               habilita: habilita
            },function(res){
                $("#mensagem").remove();
                if(res == 'OK'){
                    $('.divPainel').prepend('<div id="mensagem"><p>Configuração alterada com sucesso</p></div>');
                }else{
                 $('.divPainel').prepend('<div id="mensagem"><p>Erro na atualização do registro</p></div>');}
            }); 
        }
    });

    $( 'body.alertas .btnRestaurar' ).click( function(event) {
        event.preventDefault();
        href = $(this).attr('href');
        site_url = $('.breadcrumb a').first().attr('href');
        url = site_url + '/@@admin-alertas';
        var form = $('<form action="' + url + '" method="post">' +
                     '<input type="text" name="href" value="' + href + '" />' +
                     '</form>');
        $('body').append(form).hide();
        form.submit();
        return false
    })
    $( 'body.alertas .btnEnviar' ).click( function() {
        img = $('.listIcones ul li .active').attr('src');
        titulo = $('.inputTitulo').val();
        descricao = $('.inputTexto').val();
        start = $.datepicker.formatDate('mm-dd-yy', $('.startdate').datepicker('getDate'));
        timestart = $('.timestart').val();
        if (timestart) { start = start + ' ' + timestart };
        end = $.datepicker.formatDate('mm-dd-yy', $('.enddate').datepicker('getDate'));
        timeend = $('.timeend').val();
        if (timeend) { end = end + ' ' + timeend };
        site_url = $('.breadcrumb a').first().attr('href');
        url = site_url + '/@@criar-alertas';
        $.post( url,
        {
            img: img,
            titulo: titulo,
            descricao: descricao,
            start: start,
            end: end 
        })
        if (img && titulo && descricao) {
            $('.divPainel').prepend('<div id="mensagem"><p>Alerta cadastrado com sucesso</p></div>');
        }
    })
    $('.boxAtivo .btnSalvar').click(function() {
        desativar = $('.divBorderCheck input').is(":checked");
        if (desativar) {
            id = $('.divBorderCheck input').attr('class');
            site_url = $('.breadcrumb a').first().attr('href');
            url = site_url + '/@@lista-alertas';
            var form = $('<form action="' + url + '" method="post">' +
                         '<input type="text" name="id" value="' + id + '" />' +
                         '</form>');
            $('body').append(form).hide();
            form.submit();
        }
    })
    $('.menuAcoes .btnExcluir').click(function(e) {
        e.preventDefault();
        desativar = $('.divBorderCheck input').is(":checked");
        id = $(this).attr('href');
        site_url = $('.breadcrumb a').first().attr('href');
        url = site_url + '/@@lista-alertas/?id=' + id;
        var form = $('<form action="' + url + '" method="post">' +
                     '<input type="text" name="del_id" value="' + id + '" />' +
                     '</form>');
        $('body').append(form).hide();
        form.submit();
        return false
    })
    $('.listPainel li a').click(function(e) {
        e.preventDefault();
        painel = $(this).attr('id');
        id = $(this).attr('id');
        url = $(this).attr('href');
        var form = $('<form action="' + url + '" method="post">' +
                     '<input type="text" name="id" value="' + id + '" />' +
                     '</form>');
        $('body').append(form).hide();
        form.submit();
        return false
    })
    $('body.spagora .btnEnviar').click(function() {
        id = $('#painel-id').val();
        site_url = $('.breadcrumb a').first().attr('href');
        url = site_url + '/admin-spagora-editar-painel';
        titulo = $('.inputText').val();
        ativarEdicao = $('.ativarEdicao').is(":checked")
        ativarEdicao ? ativarEdicao = ativarEdicao : ativarEdicao = ''
        texto = $('.inputTexto').val();
        editar = 'True'
        console.log('id = ' + id + ', titulo = '+titulo+', ativarEdicao = '+ativarEdicao+', texto = '+texto);
        $.post( url,
        {
            painelid: id,
            titulo: titulo,
            ativarEdicao: ativarEdicao,
            texto: texto,
            editar: editar
        })
        $('.divPainel').prepend('<div id="mensagem"><p>Painel atualizado com sucesso</p></div>');
    })
});
