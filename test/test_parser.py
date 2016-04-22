from unittest import TestCase

from app.parsing.finder import Finder
from app.parsing.parser import Parser, Tag


class TestParser(TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_short_div(self):
        data = '''
            <div id="cookies-disabled-alert" class="alert center hide"
            style="margin: 55px auto 0; width: 600px;">
            '''
        expected_element_list = [Tag(tagname="div", attributes={'id': 'cookies-disabled-alert',
                                                                'class': 'alert center hide',
                                                                'style': 'margin: 55px auto 0; width: 600px;'})]
        real_element_list = self.parser.parse(data)
        self.assertEqual(real_element_list[0].tagname,
                         expected_element_list[0].tagname)
        self.assertEqual(real_element_list[0].attributes,
                         expected_element_list[0].attributes)

    def test_alert(self):
        data = '''
        <haha>
        <script type="text/javascript">
            alert("</script>") ;io;a <div>
        </script>
            '''

        real_element_list = self.parser.parse(data)
        print(real_element_list)

    def test_script(self):
        data = '''
            <html>
            <script type="text/javascript">
            haha<>

            </script>
            </html>
            '''
        real_element_list = self.parser.parse(data)
        print(real_element_list)

    def test_simple_script(self):
        data = '''
            <script>
            a
            </script>
            '''
        real_element_list = self.parser.parse(data)
        print(real_element_list)

    def test_virus_total(self):
        data = '''




<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <title>


Antivirus scan for 70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf at
2016-04-17 09:21:07 UTC - VirusTotal


  </title>

  <meta http-equiv="Content-type" content="text/html; charset=utf-8">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Pragma" content="no-store">
  <meta http-equiv="Expires" content="-1">
  <meta name="keywords"
        content="virustotal, antivirus, infected, free, scan, online, malware,
        malicious, scanner">
  <meta name="google-site-verification" content="Id8gKYyQBVmhsuWOE1SDkhDhAU5QW9pREnc-RO9lPLQ" />

  <meta name="description"
        content="


VirusTotal's antivirus scan report for the file with MD5 6f0b1068d531ef1f9f659bb7cd6675d9 at
2016-04-17 09:21:07 UTC.

  0 out of 57 antivirus
  detected the file as malicious.



">

  <link rel="shortcut icon" href="https://virustotalcloud.appspot.com/static/img/favicon.ico">
  <link rel="icon" href="https://virustotalcloud.appspot.com/static/img/favicon.ico" type="image/x-icon">

  <style type="text/css">
    .ltr {
      direction: ltr !important;
      text-align: left !important;
    }
    .ltr th, .ltr td {
      direction: ltr !important;
      text-align: left !important;
    }
  </style>


  <link rel="stylesheet"
        type="text/css"
        href="https://virustotalcloud.appspot.com/static/css/bootstrap.min.css?20150630">


  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js">
  </script>
  <script type="text/javascript">
    if (typeof jQuery == 'undefined'){
      document.write(unescape("%3Cscript src='https://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.7.1.min.js' type='text/javascript'%3E%3C/script%3E"));
    }
  </script>
  <script src="https://virustotalcloud.appspot.com/static/js/bootmin-2013092601.js"></script>
  <script src="https://virustotalcloud.appspot.com/static/js/base.min-2013121902.js"></script>



<script src="https://virustotalcloud.appspot.com/static/js/jquery.tablesorter.min.js"></script>
<script src="https://virustotalcloud.appspot.com/static/tiny_mce/jquery.tinymce.js?v=7"></script>
<script src="https://virustotalcloud.appspot.com/static/js/jquery.stream.js?v=9"></script>

<script type="text/javascript">

var collapseBasicInfo = true;

var mustRefresh = false;


function load(tab, url) {

  $('#' + tab + '-list').stream({
    url: url,
    page: 1,
    show: {
      waiting: '#' + tab + '-wait',
      empty: '#no-' + tab,
      more: '#btn-more-' + tab,
      error: '#' + tab + '-error'
    }
  }).stream('start');
}

function more(tab) {

  $('#' + tab + '-list').stream('more');
}

function show_votes() {

  $.ajax({
    type: 'GET',
    async: true,
    url: $('#votes-resume').attr('url'),
    dataType: 'json',
    cache: false,
    success: function(response) {
      $('#votes-resume').html(response.html)
      $.each($('.popover-spot'), function (index, element) {
        $(element).popover();
      });
    }
  }); // $.ajax()
}

function refresh(lastStatus) {

  var data = {};

  if (lastStatus)
      data = {'last-status': lastStatus};

  var request = $.ajax({
      type: 'GET',
      async: true,
      url: window.location.pathname + 'info/',
      data: data,
      dataType: 'json',
      cache: false,
      success: function(response) {

        if (response.info) {
          $('#basic-info').html(response.info);
          if (!collapseBasicInfo) {
            $('#basic-info .collapsable').show();
          }
        }

        if (response.results) {
          $('#tabs').show();
          $('div#results').html(response.results);
          $('table#antivirus-results').tablesorter();
        }

        if (response.additional) {
          $('div#tools').html(response.additional);
          $('#tabs').show();
          $('#tab-additional-info').show();
        }

        if (response.show_details_tab) {
          $('div#item-detail-content').html(response.item_detail);
          $('#item-detail-wait').hide();
          $('a[tab=item-detail]').attr('url', '');
          $('#tabs').show();
          $('#tab-item-detail').show();
        }

        if (response.show_relationships_tab) {
          $('div#item-relationships-content').html(response.item_relationships);
          $('#item-relationships-wait').hide();
          $('a[tab=item-relationships]').attr('url', '');
          $('#tabs').show();
          $('#tab-item-relationships').show();
        }

        if ($('#tab-item-behaviour').hasClass('hide') && (response.behaviour != undefined)) {
          $('#behavioural-info').html(response.behaviour);
          $('#tabs').show();
          $('#tab-item-behaviour').show();
        }

        if ($('#basic-info .collapsable').length == 0) {
          $('#toggle-details').hide();
        } else {
          $('#toggle-details').show();
        }

        if (response.status == 'completed') {
          $('#message').fadeOut(1500);
          show_votes();
        }
        else if(response.status == 'failed') {
          window.location = response.analysis_failed_url;
        }
        else {
          window.setTimeout(function() {
            refresh(response.status);
          }, response.refresh);
        }

    },
    error: function() {
      window.setTimeout(function() { refresh(lastStatus); }, 3000);
    }
  }); // $.ajax()
}

$('.expand-data').live('click', function(e){
  e.preventDefault();
  var canvas = $(this).parents('.expand-canvas');
  canvas.find('.hide').toggle();
  $(this).toggleClass('text-bold')
});

$('.showall').live('click', function(){
  var currentText = $.trim($(this).html());
  if (currentText == 'Show all') {
    $(this).parents('.expandable').find('.toggable').show();
    $(this).html('Contract')
  } else {
    $(this).parents('.expandable').find('.toggable').hide();
    $(this).html('Show all')
  }
});

$(document).ready(function(){

  $('table#antivirus-results').tablesorter();



    show_votes();

    if ($('#basic-info .collapsable').length == 0) {
      $('#toggle-details').hide();
    }



    $(document).delegate('.vote', 'click', function() {
      var vote = $(this).attr('vote');
      var button = $(this);
      var animation = window.setInterval(function () {
        button.animate({ opacity: 0.2 }, 450).animate({ opacity: 1 }, 450);
      }, 1000);

      $.ajax({
        type: 'POST',
        async: true,
        url: $(this).attr('url'),
        dataType: 'json',
        context: this,
        cache: false,
        success: function(response) {
          $('#votes-resume').html(response.html)
          window.clearInterval(animation);
            $('.popover').hide();
          }
      }); // $.ajax()
    })

    $('#toggle-details').click(function() {

      collapseBasicInfo = !collapseBasicInfo;
      $(this).toggleClass('less');

      if (collapseBasicInfo) {
        $('#basic-info .collapsable').hide();
        $(this).html('More details')
      }
      else {
        $('#basic-info .collapsable').show();
        $(this).html('Less details')
      }
    });

    $('a[data-toggle="tab"]').on('shown', function (e) {

      var tab_object = $(e.target);
      var tab = tab_object.attr('tab');
      var url = tab_object.attr('url');

      if (url == undefined || url == ''){
        return
      }

      if (tab == 'additional-info') {

        $('#additional-info-error').hide();
        $('#additional-info-wait').show();

        $.ajax({
          type: 'GET',
          async: true,
          url: url,
          dataType: 'json',
          context: this,
          success: function(response){
            if (response.additional_info) {
              $('#additional-info-wait').hide();
              $('div#additional-info-content').html(response.additional_info);
            }
          },
          error: function() {
            $('#additional-info-wait').hide();
            $('#additional-info-error').show();
          }
        }); // $.ajax()

      } else if (tab == 'item-detail') {

        $('#item-detail-error').hide();
        $('#item-detail-wait').show();

        $.ajax({
          type: 'GET',
          async: true,
          url: url,
          dataType: 'json',
          context: this,
          success: function(response){
            if (response.item_detail) {
              $('#item-detail-wait').hide();
              $('div#item-detail-content').html(response.item_detail);
              tab_object.attr('url', '');
            }
          },
          error: function() {
            $('#item-detail-wait').hide();
            $('#item-detail-error').show();
          }
        }); // $.ajax()

      } else {  // comments or votes
          load(tab, url);
      }
    });

    // initialize comment editor

    var t = $('textarea.tinymce');

    if (t) {

      t.tinymce({

        script_url : 'https://virustotalcloud.appspot.com/static/tiny_mce/tiny_mce.js',

        // General options
        theme : "advanced",
        mode: "none",
        plugins : "bbcode,paste",

        paste_text_sticky : true,

        setup : function(ed) {
            ed.onInit.add(function(ed) {
              ed.pasteAsPlainText = true;
            });
        },

        // Theme options
        theme_advanced_buttons1 : "bold,italic,underline,undo,redo,styleselect,removeformat",
        theme_advanced_buttons2 : "",
        theme_advanced_buttons3 : "",
        theme_advanced_buttons4 : "",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_styles : "Code=codeStyle;Quote=quoteStyle",
        theme_advanced_resizing : false,

        content_css : "https://virustotalcloud.appspot.com/static/css/bbcode.css",
        entity_encoding : "raw",
        add_unload_trigger : false,
        remove_linebreaks : false,
        inline_styles : false,
        convert_fonts_to_spans : false
      });
    }

    // load comments

    load('comments', $('a[tab="comments"]').attr('url'));

    // setup handlers

    $(document).delegate('.vote-comment', 'click', function (event) {
      $.ajax({
        type: 'POST',
        async: true,
        url: $(this).attr('url'),
        dataType: 'json',
        success: function(response){
            $('span#' + response.comment_id + '-'
                      + response.vote).html(response[response.vote])
        }
      });
      event.preventDefault();
    });

    $(document).delegate('.delete-comment', 'click', function (event) {
      $.ajax({
        type: 'POST',
        async: true,
        url: $(this).attr('url'),
        dataType: 'json',
        success: function(response) {
          $('.comment#' + response.comment_id).fadeOut();
        }
      });
      event.preventDefault();
    });

    $(document).delegate('.delete-vote', 'click', function (event) {
      $.ajax({
        type: 'POST',
        async: true,
        url: $(this).attr('url'),
        dataType: 'json',
        success: function(response) {
          $('.vote#' + response.vote_id).fadeOut();
          // Refresh the votes indicator;
          show_votes();
        }
      });
      event.preventDefault();
    });


    $(document).delegate('#btn-post-comment', 'click', function (event) {
      $.ajax({
        type: 'POST',
        async: true,
        url: $(this).attr('url'),
        data: {'comment': $('textarea#comment').val(), 'page': 1},
        dataType: 'html',
        success: function(response) {
          $('#no-comments').hide();
          $('#comments-list').prepend(response);
        }
      });
      event.preventDefault();
    });

    $(document).delegate('#btn-more-comments', 'click', function (event) {
      $('#comments-wait').show();
      $('#comments-list').stream('more');
      event.preventDefault();
    });

    $(document).delegate('#btn-more-votes', 'click', function (event) {
      $('#votes-wait').show();
      $('#votes-list').stream('more');
      event.preventDefault();
    });

  });
</script>



  <script type="text/javascript" async>
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-27433547-2']);
    _gaq.push(['_setDomainName', '.virustotal.com']);
    _gaq.push(['_trackPageview']);

    (function() {
      var ga = document.createElement('script');
      ga.type = 'text/javascript';
      ga.async = true;
      ga.src = ('https:' == document.location.protocol ?
                'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(ga, s);
    })();
  </script>

</head>

<body >
  <div class="wrapper">
    <div id="cookies-disabled-alert" class="alert center hide"
         style="margin: 55px auto 0; width: 600px;">
      <a class="close" data-dismiss="alert">×</a>
      <strong>Cookies are disabled!</strong>
      This site requires cookies to be enabled to work properly
    </div>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">



<ul class="nav">
  <li id="mnu-home">
		<a href="/en/" alt="home" title="Home"><i class="icon-home icon-white" alt="home" title="Home"></i></a>
	</li>
  <li id="mnu-community">
  	<a href="/en/community/">Community</a>
  </li>
  <li id="mnu-statistics">
  	<a href="/en/statistics/">Statistics</a>
  </li>
  <li id="mnu-documentation" class="dropdown">
  	<a href="/en/documentation/">Documentation</a>
  </li>
  <li id="mnu-faq">
  	<a href="/en/faq/">FAQ</a>
  </li>
  <li id="mnu-about">
  	<a href="/en/about/">About</a>
  </li>
</ul>


  <ul class="nav pull-right">


    <li>
      <a id="mnu-join" data-toggle="modal" data-backdrop="static"
         data-keyboard="true" href="#dlg-join">
        Join our community
      </a>
    </li>
    <li id="mnu-signin" class="">
      <a data-toggle="modal" data-backdrop="static"
         data-keyboard="true" href="#dlg-signin">
        Sign in
      </a>
    </li>

  </ul>



<ul class="nav pull-right">
  <li id="mnu-language" class="dropdown">
    <a class="dropdown-toggle" data-toggle="dropdown" href="#">


      <i class="icon-flag"></i> English
    </a>
    <ul class="dropdown-menu">
      <li>
        <div class="row-fluid" style="width: 300px;">
          <ul class="unstyled span6">
            <li><a class="set-language" href="/ca/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Català</a></li>
            <li><a class="set-language" href="/da/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Dansk</a></li>
            <li><a class="set-language" href="/de/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Deutsch</a></li>
            <li><a class="set-language" href="/en/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">English</a></li>
            <li><a class="set-language" href="/es/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Español</a></li>
            <li><a class="set-language" href="/fr/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Français</a></li>
            <li><a class="set-language" href="/hr/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Hrvatski</a></li>
            <li><a class="set-language" href="/it/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Italiano</a></li>
            <li><a class="set-language" href="/hu/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Magyar</a></li>
            <li><a class="set-language" href="/nl/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Nederlands</a></li>
            <li><a class="set-language" href="/nb/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Norsk</a></li>
            <li><a class="set-language" href="/pt/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Português</a></li>
            <li><a class="set-language" href="/pl/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Polski</a></li>
            <li><a class="set-language" href="/sk/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Slovenčina</a></li>
          </ul>
          <ul class="unstyled span6">
            <li><a class="set-language" href="/uk/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Українська</a></li>
            <li><a class="set-language" href="/vi/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Tiếng Việt</a></li>
            <li><a class="set-language" href="/tr/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Türkçe</a></li>
            <li><a class="set-language" href="/ru/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Русский</a></li>
            <li><a class="set-language" href="/sr/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">Српски</a></li>
            <li><a class="set-language" href="/bg/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">български език</a></li>
            <li><a class="set-language" href="/he/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">עברית</a></li>
            <li><a class="set-language" href="/ka/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">ქართული</a></li>
            <li><a class="set-language" href="/ar/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">اللغة العربية</a></li>
            <li><a class="set-language" href="/fa/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">فارسی</a></li>
            <li><a class="set-language" href="/zh-cn/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">简体中文</a></li>
            <li><a class="set-language" href="/zh-tw/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">繁體中文</a></li>
            <li><a class="set-language" href="/ja/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">日本語</a></li>
            <li><a class="set-language" href="/ko/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/analysis/">한국어</a></li>
          </ul>
        </div>
      </li>
    </ul>
  </li>
</ul>




        </div>
      </div>
    </div>


<div id="dlg-ciphered-bundle" class="modal hide">

  <div class="modal-header">
    <a class="close" href="">×</a>
    <h3><i class="icon-lock"></i> Ciphered bundle</h3>
  </div>
  <div class="modal-body">
    <p>

      The submitted file is a compressed bundle ciphered with password <em>infected</em>,
      do you want to display the report for the contained inner file?

    </p>
  </div>

  <div class="modal-footer">
    <a id="ciphered-this" class="btn cancel" href="">
      Compressed file
    </a>
    <a id="btn-ciphered-inner" class="btn btn-primary"
       href="">
      Inner file
    </a>
  </div>

</div>

<div class="container" style="padding:40px 0">
  <div class="clearfix">
    <div class="margin-top-2">
      <a href="/en/">
        <img src="https://virustotalcloud.appspot.com/static/img/logo-small.png" alt="VirusTotal">
      </a>
    </div>
  </div>

  <div class="frame" style="margin:20px 0">
    <div id="basic-info">








<div class="row">
  <div class="span8 columns">
    <table style="margin-bottom:8px;margin-left:8px;">
      <tbody>

        <tr>
          <td>SHA256:</td>
          <td>
            70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf
          </td>
        </tr>


        <tr>
          <td>File name:</td>
          <td>zadanie.pdf</td>
        </tr>



        <tr>
          <td>Detection ratio:</td>
          <td class=" text-green
                      ">
            0 / 57
          </td>
        </tr>



        <tr>
          <td>Analysis date:</td>
          <td >
            2016-04-17 09:21:07 UTC

            ( 5 days, 4 hours ago )


          </td>
        </tr>

      </tbody>
    </table>
  </div>

  <div id="votes-resume" class="pull-right margin-right-1"
    url="/en/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/votes-resume/">
  </div>

</div>








    </div>
  </div>

  <ul id="tabs" class="nav nav-tabs" style="float:none">
    <li class="active">
      <a href="#analysis" data-toggle="tab" tab="analysis">
        <i class="icon-list-alt"></i> Analysis
      </a>
    </li>
    <li id="tab-item-detail"
        >
      <a href="#item-detail" data-toggle="tab" tab="item-detail"
        >
        <i class="icon-zoom-in"></i> File detail
      </a>
    </li>
    <li id="tab-item-relationships" class="hide">
      <a href="#item-relationships" data-toggle="tab" tab="item-relationships" >
        <i class="icon-random"></i> Relationships
      </a>
    </li>
    <li>
      <a href="#additional-info" data-toggle="tab" tab="additional-info"
         >
        <i class="icon-info-sign"></i> Additional information
      </a>
    </li>
    <li>
      <a href="#comments" data-toggle="tab" tab="comments"
         url="/en/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/comments/?page={page}">
         <i class="icon-comment"></i> Comments
         <span class="badge badge-info"
               style="margin:0 5px">0</span>
      </a>
    </li>
    <li>
      <a href="#votes" data-toggle="tab" tab="votes"
         url="/en/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/votes/?page={page}">
         <i class="icon-thumbs-down"></i> Votes
      </a>
    </li>
    <li id="tab-item-behaviour" class="hide">
      <a href="#behavioural-info" data-toggle="tab" tab="behavioural-info">
        <i class="icon-film"></i> Behavioural information
      </a>
    </li>
  </ul>

  <div class="tab-content" style="overflow:visible">

    <div class="tab-pane active" id="analysis">
      <div id="results">





<div id="active-tab">

  <table class="table table-striped" id="antivirus-results">
    <thead>
      <tr>
        <th class="header headerSortDown vt-width-30">
          Antivirus
        </th>
        <th id="results-header" style="cursor:pointer;">
          Result
        </th>
        <th>
          Update
        </th>
      </tr>
    </thead>
    <tbody>


      <tr>
          <td class="ltr">
            ALYac
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            AVG
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            AVware
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Ad-Aware
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            AegisLab
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            AhnLab-V3
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Alibaba
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160415
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Antiy-AVL
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Arcabit
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Avast
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Avira (no cloud)
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Baidu
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Baidu-International
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            BitDefender
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Bkav
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160415
          </td>
      </tr>

      <tr>
          <td class="ltr">
            CAT-QuickHeal
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            CMC
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160415
          </td>
      </tr>

      <tr>
          <td class="ltr">
            ClamAV
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Comodo
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Cyren
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            DrWeb
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            ESET-NOD32
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Emsisoft
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            F-Prot
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            F-Secure
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Fortinet
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            GData
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Ikarus
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Jiangmin
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            K7AntiVirus
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            K7GW
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Kaspersky
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Kingsoft
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Malwarebytes
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            McAfee
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            McAfee-GW-Edition
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            eScan
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Microsoft
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            NANO-Antivirus
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Panda
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Qihoo-360
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Rising
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            SUPERAntiSpyware
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Sophos
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Symantec
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Tencent
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            TheHacker
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            TotalDefense
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            TrendMicro
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            TrendMicro-HouseCall
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            VBA32
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160415
          </td>
      </tr>

      <tr>
          <td class="ltr">
            VIPRE
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            ViRobot
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Yandex
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Zillya
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160416
          </td>
      </tr>

      <tr>
          <td class="ltr">
            Zoner
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160417
          </td>
      </tr>

      <tr>
          <td class="ltr">
            nProtect
          </td>
          <td class="ltr text-green">

              <i data-toggle="tooltip" title="File not detected" class="icon-ok-sign" alt="clean"></i>

          </td>
          <td class="ltr">
            20160415
          </td>
      </tr>


    </tbody>
  </table>
</div>
<script>
  $('.tooltip').hide();
  $("i[data-toggle=tooltip]").tooltip();
  $("span[data-toggle=tooltip]").tooltip();
</script>


      </div>
    </div>

    <div class="tab-pane extra-info" id="item-detail">

      <div id="item-detail-wait" class="center hide" >
        <img style="padding: 10px 10px;" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
      </div>

      <div id="item-detail-error" class="center" style="display:none">
        An error occurred
      </div>

      <div id="item-detail-content">



<div id="file-details">









<div class="alert">
  <strong>The file being studied is a PDF document!</strong>
  The document's header reveals it is using the following file format
  specification: <strong>%PDF-1.4</strong>.
</div>


<h5><i class="icon-file"></i> PDFiD information</h5>
<div class="enum-container">














<div class="enum"><i class="icon-info-sign"></i> This PDF document
  has 1 page,
  please note that most malicious PDFs have only one page.
</div>

<div class="enum"><i class="icon-info-sign"></i> This PDF document
  has 7 object start declarations and
 7 object end declarations.
</div>
<div class="enum"><i class="icon-info-sign"></i> This PDF document
  has 2 stream object start declarations
  and 2 stream object end
  declarations.
</div>

<div class="enum"><i class="icon-info-sign"></i> This PDF document has a cross
  reference table (xref).
</div>


<div class="enum"><i class="icon-info-sign"></i> This PDF document has a pointer
  to the cross reference table (startxref).
</div>


<div class="enum"><i class="icon-info-sign"></i> This PDF document has a
  trailer dictionary containing entries allowing the cross reference table,
  and thus the file objects, to be read.
</div>

</div>



<h5><i class="icon-eye-open"></i> ExifTool file metadata</h5>


<div class="enum">
  <div class="floated-field-key">MIMEType</div>
  <div class="floated-field-value">application/pdf</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">XMPToolkit</div>
  <div class="floated-field-value">XMP toolkit 2.9.1-13, framework 1.6</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">About</div>
  <div class="floated-field-value">uuid:3b4436aa-7b59-11e5-0000-91eeaaf82182</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">ModifyDate</div>
  <div class="floated-field-value">2015:10:22 22:44:28+02:00</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Description</div>
  <div class="floated-field-value">()</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Producer</div>
  <div class="floated-field-value">GPL Ghostscript 9.07</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Creator</div>
  <div class="floated-field-value">x</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">CreateDate</div>
  <div class="floated-field-value">2015:10:22 22:44:28+02:00</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Author</div>
  <div class="floated-field-value">x</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Linearized</div>
  <div class="floated-field-value">No</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Keywords</div>
  <div class="floated-field-value">()</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">FileTypeExtension</div>
  <div class="floated-field-value">pdf</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">PageCount</div>
  <div class="floated-field-value">1</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Title</div>
  <div class="floated-field-value">D:\DokumentyOla\Drawing1 Model (1)</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">Format</div>
  <div class="floated-field-value">application/pdf</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">PDFVersion</div>
  <div class="floated-field-value">1.4</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">FileType</div>
  <div class="floated-field-value">PDF</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">DocumentID</div>
  <div class="floated-field-value">uuid:3b4436aa-7b59-11e5-0000-91eeaaf82182</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">CreatorTool</div>
  <div class="floated-field-value">PDFCreator Version 1.7.1</div>
  <br style="clear:both;"/>
</div>








</div>

<script>
  $("div[rel=tooltip]").tooltip();
</script>

      </div>

    </div>

    <div class="tab-pane" id="item-relationships">

      <div id="item-relationships-wait" class="center hide" >
        <img style="padding: 10px 10px;" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
      </div>

      <div id="item-relationships-error" class="center" style="display:none">
        An error occurred
      </div>

      <div id="item-relationships-content" class="extra-info">

      </div>

    </div>

    <div class="tab-pane" id="additional-info">

      <div id="additional-info-wait" class="center hide" >
        <img style="padding: 10px 10px;" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
      </div>

      <div id="additional-info-error" class="center" style="display:none">
        An error occurred
      </div>

      <div id="additional-info-content">






<div id="file-details" class="extra-info">

<h5><i class="icon-question-sign"></i> File identification</h5>
<div class="enum-container">
<div class="enum">
  <span class="field-key">MD5</span> 6f0b1068d531ef1f9f659bb7cd6675d9
</div>
<div class="enum">
  <span class="field-key">SHA1</span> a70371250bc51d236e3040a95d6dde0d5b87c164
</div>
<div class="enum">
  <span class="field-key">SHA256</span> 70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf
</div>
<div class="enum">
  <div class="floated-field-key">ssdeep</div>
  <div class="floated-field-value">3072:DY3BNCr31fFA3Dj3PiN/WnFVQVFhhaWn4:s3a/GX3P4AWQWn4</div>
  <br style="clear:both;" />
</div>


<div class="enum">
  <span class="field-key">File size</span>
  102.3 KB ( 104773 bytes )
</div>
<div class="enum">
  <span class="field-key">File type</span> PDF
</div>
<div class="enum">
  <div class="floated-field-key">Magic literal</div>
  <div class="floated-field-value">PDF document, version 1.4</div>
  <br style="clear:both;" />
</div>
<div class="enum">
  <table>
    <tr>
      <td class="field-key">TrID</td>
      <td class="field-value">

        Adobe Portable Document Format (100.0%)<br/>

      </td>
    </tr>
  </table>
</div>

<div class="enum">
  <div class="floated-field-key">Tags</div>
  <div class="floated-field-value">

    <span class="label label-info">pdf</span>

  </div>
  <br style="clear:both;" />
</div>

</div>







<h5><i class="icon-ticket"></i> VirusTotal metadata</h5>
<div class="enum-container">
<div class="enum">
  <span class="field-key">First submission</span>
  2016-03-16 22:56:37 UTC ( 1 month ago )
</div>
<div class="enum">
  <span class="field-key">Last submission</span>
  2016-03-16 22:56:37 UTC ( 1 month ago )
</div>

<div class="enum">
  <table>
    <tr>
      <td class="field-key">File names</td>
      <td class="field-value">

        zadanie.pdf<br/>

      </td>
    </tr>
  </table>
</div>

</div>










<h5><i class="icon-eye-open"></i> ExifTool file metadata</h5>
<div class="enum-container">


<div class="enum">
  <div class="floated-field-key">MIMEType</div>
  <div class="floated-field-value">application/pdf</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">XMPToolkit</div>
  <div class="floated-field-value">XMP toolkit 2.9.1-13, framework 1.6</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">About</div>
  <div class="floated-field-value">uuid:3b4436aa-7b59-11e5-0000-91eeaaf82182</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">ModifyDate</div>
  <div class="floated-field-value">2015:10:22 22:44:28+02:00</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Description</div>
  <div class="floated-field-value">()</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Producer</div>
  <div class="floated-field-value">GPL Ghostscript 9.07</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Creator</div>
  <div class="floated-field-value">x</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">CreateDate</div>
  <div class="floated-field-value">2015:10:22 22:44:28+02:00</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Author</div>
  <div class="floated-field-value">x</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Linearized</div>
  <div class="floated-field-value">No</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Keywords</div>
  <div class="floated-field-value">()</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">FileTypeExtension</div>
  <div class="floated-field-value">pdf</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">PageCount</div>
  <div class="floated-field-value">1</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Title</div>
  <div class="floated-field-value">D:\DokumentyOla\Drawing1 Model (1)</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">Format</div>
  <div class="floated-field-value">application/pdf</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">PDFVersion</div>
  <div class="floated-field-value">1.4</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">FileType</div>
  <div class="floated-field-value">PDF</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">DocumentID</div>
  <div class="floated-field-value">uuid:3b4436aa-7b59-11e5-0000-91eeaaf82182</div>
  <br style="clear:both;" />
</div>



<div class="enum">
  <div class="floated-field-key">CreatorTool</div>
  <div class="floated-field-value">PDFCreator Version 1.7.1</div>
  <br style="clear:both;" />
</div>


</div>


</div>


      </div>

    </div>

    <div class="tab-pane" id="comments">

      <div id="no-comments" class="hide alert alert-info">
        <strong>No comments.</strong>
        No VirusTotal Community member has commented on this item yet, be the first one to do so!
      </div>

      <div id="comments-list" class="user-list">
      </div>

      <div id="comments-wait" class="center" style="display:none">
        <img style="padding: 10px 10px;" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
      </div>

      <div class="margin-top-2">
        <a id="btn-more-comments" class="btn small hide" href="#">
          More comments
        </a>
      </div>

      <div id="comment-editor"
           class="margin-top-2  hide ">

        <h3 class="pull-left">Leave your comment...</h3>
        <span id="comment-help" class="label pull-left" rel="popover"
              data-original-title="Hashtags and mentions"
              data-placement="bottom"
              data-content="You can use Twitter-style hashtags in your comments (i.e. #goodware, #malware). You can also address comments to particular users by prepending the @ character to the username (i.e. @JoeBrown).">?
        </span>

        <div style="clear:both">
          <textarea id="comment" class="tinymce"
                    style="width:100%; height:160px;">
          </textarea>
        </div>

        <a id="btn-post-comment" class="btn primary margin-top-2" href="#" url="/en/file/70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf/comments/post/" item-id="70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf">
          Post comment
        </a>

      </div>
      <div id="comment-signin"
           class="margin-top-2 alert alert-error ">
        <p>
          <strong>You have not signed in.</strong> Only registered users can leave comments, sign in and have a voice!
        </p>
        <div class="alert-actions">
          <a class="btn small" data-toggle="modal" data-backdrop="static"
             data-keyboard="true" href="#dlg-signin">
            Sign in
          </a>
          <a class="btn small" data-toggle="modal" data-backdrop="static"
             data-keyboard="true" href="#dlg-join">
            Join the community
          </a>
        </div>
      </div>
    </div>

    <div class="tab-pane" id="votes">

      <div id="no-votes" class="hide alert alert-info">
        <strong>No votes</strong>.
        No one has voted on this item yet, be the first one to do so!
      </div>

      <div id="votes-list" class="user-list">
      </div>

      <div id="votes-wait" class="center" style="display:none">
        <img style="padding: 10px 10px;" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
      </div>

      <div class="margin-top-2">
        <a id="btn-more-votes" class="btn small hide" href="#">
          More votes
        </a>
      </div>

    </div>

    <div class="tab-pane ltr extra-info" id="behavioural-info">

    </div>

  </div>
</div>
<script>
  $('.goto').click(function(){
    var self = $(this);
    var tab = self.attr('tab');
    var placeholder = self.attr('placeholder');
    if (tab != undefined) {
      $('a[href=' + tab + ']').click();
    }
    if (placeholder != undefined) {
      $(placeholder).localGoto();
    }
  });
</script>



    <div class="push"></div>
  </div>

  <div class="footer center">
    <a target="_blank" href="http://blog.virustotal.com">
      <i class="icon-rss"></i> Blog</a> |
    <a target="_blank" href="http://twitter.com/virustotal">
      <i class="icon-twitter"></i> Twitter</a> |
    <a href="/en/about/contact/" alt="Contact">
      <i class="icon-envelope-alt"></i> <span class="contact"></span>
    </a> |
    <a target="_blank" href="http://groups.google.com/forum/#!forum/virustotal">
      <i class="icon-group"></i> Google groups</a> |
    <a href="/en/about/terms-of-service/">
      <i class="icon-legal"></i>  ToS</a> |
    <a href="/en/about/privacy/">
      <i class="icon-lock"></i>  Privacy policy</a>
  </div>


<div id="dlg-password-reset" class="modal hide">


<div class="modal-header">
  <a class="close" href="/en/">×</a>
  <h3>Recover your password</h3>
</div>

<div class="modal-body">
  <p style="margin-bottom:20px">
    Enter the email address associated to your VirusTotal Community account and we'll send you a message so you can setup a new password.
  </p>

  <form id="frm-password-reset" method="post" class="form-horizontal"
        action="/en/account/reset-password/">

    <fieldset>
      <div class="control-group">
        <label class="control-label" for="email">
          Email:
        </label>
        <div class="controls">
          <input type="text" id="email" name="email" class="input-xlarge"
                 value="">
          <div style="width:300px">

          </div>
        </div>
      </div>
    </fieldset>
  </form>
</div>

<div class="modal-footer">
  <img width="16" height="16" class="loading hide" alt="loading"
       src="https://virustotalcloud.appspot.com/static/img/wait.gif" style="padding-top:7px; float:left"/>

  <a id="btn-recover" class="btn btn-primary"
     href="javascript:resetPassword()">
    Recover password
  </a>

  <a class="btn cancel secondary" href="/en/">
    Cancel
  </a>
</div>
</div>

<div id="dlg-join" class="modal hide">


<div class="modal-header">
  <a class="close" href="/en/">×</a>
  <h3>Join VirusTotal Community</h3>
</div>

<div class="modal-body">

  <p style="margin-bottom:14px">
     Interact with other VirusTotal users and have an active voice when fighting today's Internet threats.
    <a href="/en/documentation/virustotal-community/">
      Find out more about VirusTotal Community.
    </a>
  </p>

  <form id="frm-join" method="post" class="form-horizontal"
        action="/en/account/signup/">
    <fieldset style="margin:0">

      <div class="control-group">
        <label class="control-label" for="first_name">
          First name
        </label>
        <div class="controls">
          <input type="text" id="first_name" name="first_name"
                 class="input-xlarge" value="">

        </div>
      </div>

      <div class="control-group">
        <label class="control-label" for="last_name">
          Last name
        </label>
        <div class="controls">
          <input type="text" id="last_name" name="last_name"
                 class="input-xlarge" value="">

        </div>
      </div>

      <div class="control-group">
        <label class="control-label" for="username">
          Username
        </label>
        <div class="controls">
            <input type="text" id="username" name="username"
                  class="input-xlarge" value="">
            <span class="required-field">*</span>

        </div>
      </div>

      <div class="control-group">
        <label class="control-label" for="email">
          Email
        </label>
        <div class="controls">
          <input type="text" id="email" name="email" class="input-xlarge"
                 value="">
          <span class="required-field">*</span>

        </div>
      </div>

      <div class="control-group">
        <label class="control-label" for="password">
          Password
        </label>
        <div class="controls">
          <input type="password" id="password1" name="password1"
                 class="input-xlarge" value="">
          <span class="required-field">*</span>

        </div>
      </div>

      <div class="control-group">
        <label class="control-label" for="password2">
          Confirm password
        </label>
        <div class="controls">
          <input type="password" id="password2" name="password2"
                 class="input-xlarge" value="">
          <span class="required-field">*</span>
        </div>
      </div>

      <span class="required-field margin-left-15">*</span>
      Required field

    </fieldset>
  </form>
</div>

<div class="modal-footer">
  <img width="16" height="16" class="loading hide pull-left margin-top-1"
       alt="loading" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
  <a class="btn cancel" href="/en/">
    Cancel
  </a>
  <a id="btn-join" class="btn btn-primary" href="javascript:signup()">
    Sign up
  </a>
</div>
</div>

<div id="dlg-signin" class="modal hide">


<div class="modal-header">
  <a class="close" href="/en/">×</a>
  <h3>Sign in</h3>
</div>
<div class="modal-body">

  <div class="margin-left-3 margin-bottom-2">

  </div>

  <form id="frm-signin" method="post" class="form-horizontal"
        action="/en/account/signin/">

    <div class="dlg-signin-content">
      <fieldset>
        <div class="control-group">
          <label class="control-label" for="username">
            Username or email
          </label>
          <div class="controls">
            <input type="text" class="input-xlarge" id="username"
                   name="username" value="">

          </div>
        </div>
        <div class="control-group">
          <label class="control-label" for="password">
            Password
          </label>
          <div class="controls">
            <input type="password" class="input-xlarge" id="password"
                   name="password">

          </div>
        </div>
          <a href="#" class="margin-left-15" id="lnk-password-reset">
            Forgot your password?
          </a>
      </fieldset>
    </div>
  </form>
</div>

<div class="modal-footer">
  <img width="16" height="16" class="loading hide pull-left margin-top-1"
       alt="loading" src="https://virustotalcloud.appspot.com/static/img/wait.gif"/>
  <a class="btn cancel" href="/en/">
    Cancel
  </a>
  <a id="btn-sign-in" class="btn btn-primary"
     href="javascript:signin('')">
    Sign in
  </a>
</div>
</div>





</body>
</html>


                '''
        real_element_list = self.parser.parse(data)
        finder = Finder(real_element_list)
        print(finder.content_list)