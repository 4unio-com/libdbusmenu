<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
      <head>
        <title>
    Ubuntu LDTP Tests Report
    </title>
        <!-- Launchpad style sheet -->
        <style type="text/css" media="screen, print">@import url(https://edge.launchpad.net/+icing/rev7667/+style-slimmer.css);</style>
        <!--[if lte IE 7]>
      <style type="text/css">#lp-apps span {margin: 0 0.125%;}</style>
    <![endif]-->
        <style type="text/css">
      fieldset.collapsed div, fieldset div.collapsed {display: none;}
    </style>
        <noscript>
          <style type="text/css">
        fieldset.collapsible div, fieldset div.collapsed {display: block;}
      </style>
        </noscript>
        <script type="text/javascript" src="https://edge.launchpad.net/+icing/build/launchpad.js"/>
        <script type="text/javascript">var cookie_scope = '; Path=/; Secure; Domain=.launchpad.net';</script>
        <script type="text/javascript">
      function onLoadFunction() {
        sortables_init();
        initInlineHelp();
      }
      registerLaunchpadFunction(onLoadFunction);
    </script>
        <link rel="shortcut icon" href="https://edge.launchpad.net/@@/launchpad.png"/>
      </head>
      <body id="document" class="tab-bugs onecolumn">
        <div id="locationbar">
          <div id="logincontrol">
            <a href="https://bugs.edge.launchpad.net/bugs/bugtrackers/+login">Log in / Register</a>
          </div>
          <form id="globalsearch" action="https://edge.launchpad.net/+search" xml:lang="en" lang="en" dir="ltr" method="get" accept-charset="UTF-8">
            <img src="https://edge.launchpad.net/@@/search.png" style="margin-bottom: -4px" alt="Search launchpad:"/>
            <input type="search" id="search-text" name="field.text"/>
          </form>
          <div id="lp-hierarchy" class="home">
            <a href="/" class="breadcrumb">
              <img alt="Launchpad" src="https://edge.launchpad.net/@@/launchpad-logo-and-name-hierarchy.png"/>
            </a>
          </div>
          <div id="globalheader" xml:lang="en" lang="en" dir="ltr">
            <div class="sitemessage">This site is running pre-release code. <a href="https://edge.launchpad.net/launchpad/+filebug">Please report all bugs.</a></div>
          </div>
          <div class="apps-separator">
            <!-- -->
          </div>
          <div id="lp-apps" class="clearfix">
            <!-- :-) -->
            <span class="overview">
              <a href="https://edge.launchpad.net/">Launchpad Home</a>
            </span>
            <small> / </small>
            <span class="branches" title="The Code Bazaar">
              <a href="https://code.edge.launchpad.net/">Code</a>
            </span>
            <small> / </small>
            <span class="bugs active">
              <a href="https://bugs.edge.launchpad.net/">Bugs</a>
            </span>
            <small> / </small>
            <span class="specifications" title="Launchpad feature specification tracker.">
              <a href="https://blueprints.edge.launchpad.net/">Blueprints</a>
            </span>
            <small> / </small>
            <span class="translations">
              <a href="https://translations.edge.launchpad.net/">Translations</a>
            </span>
            <small> / </small>
            <span class="answers" title="Launchpad Answer Tracker">
              <a href="https://answers.edge.launchpad.net/">Answers</a>
            </span>
          </div>
        </div>
        <!--id="locationbar"-->
        <div id="mainarea">
          <div id="container">
            <!--[if IE 7]>&nbsp;<![endif]-->
            <div id="navigation-tabs">
                          
                          
                        </div>
            <div>
              <p>
                <br/>
              </p>
              <h1>Ubuntu LDTP Tests Report</h1>
              <p>
                  This are the results from a run of Ubuntu Desktop Tests. <br/>
                  If you find false positives, please, report bugs against <a href="https://launchpad.net/ubuntu-desktop-testing/+filebug">ubuntu-desktop-testing</a> project.
              </p>
              <table width="100%" class="sortable listing" id="trackers">
                <thead>
                  <tr>
                    <th>Test Name</th>
                    <th>Script Name</th>
                    <th>Status</th>
                    <th>Time Elapsed (s)</th>
                    <th>Error</th>
                    <th>Screenshot</th>
                  </tr>
                </thead>
                <tbody>
                  <xsl:for-each select="descendant::group">
                    <xsl:for-each select="child::script/child::test">
                      <tr>
                        <td>
                          <xsl:value-of select="@name"/>
                        </td>
                        <td>
                          <xsl:value-of select="ancestor::script[last()]/@name"/>
                        </td>
                        <xsl:if test="child::pass/child::text() = 0">
                            <td><font color="red">Failed</font></td>
                        </xsl:if>
                        <xsl:if test="child::pass/child::text() = 1">
                            <td><font color="green">Passed</font></td>
                        </xsl:if>
                        <td>
                            <xsl:value-of select="child::time/child::text()"/>
                        </td>
                        <td>
                          <xsl:if test="child::pass/child::text() = 0">
                              <xsl:value-of select="child::error/child::text()"/>
                          </xsl:if>
                        </td>
                        <td>
                          <xsl:if test="child::pass/child::text() = 0">
                            <xsl:apply-templates select="child::screenshot" mode="link"/>
                          </xsl:if>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>
                </tbody>
              </table>
              <p>
                <!-- *** Last Paragraph Space *** -->
              </p>
            </div>
            <div class="clear"/>
          </div>
          <!--id="container"-->
        </div>
        <!--id="mainarea"-->
        <div id="globalfooter" class="clearfix" xml:lang="en" lang="en" dir="ltr">
          <div id="colophon"><a href="/+tour">What is Launchpad?</a>
           | <a href="https://help.launchpad.net/">Get help with Launchpad</a>
        </div>
          <div id="lp-arcana">
            Copyright 2004-2008 <a href="http://canonical.com/">Canonical Ltd.</a>
          |
          <a href="/legal">Terms of use</a>
          <span id="lp-version">
            |
            <a href="https://help.launchpad.net/LaunchpadReleases">Launchpad 2.1.12 (r76673)</a>
            
            
            beta site
          </span>
        </div>
        </div>
        <!--id="globalfooter"-->
        <div id="help-pane" class="invisible">
          <div id="help-body">
            <iframe id="help-pane-content" class="invisible" src="javascript:void(0);"/>
          </div>
          <div id="help-footer">
            <span id="help-close"/>
          </div>
        </div>
      </body>
    </html>
    <!-- at least 396 queries issued in 3.36 seconds -->
    <!-- Launchpad 2.1.12 (r7513) -->
  </xsl:template>
  <xsl:template match="screenshot" mode="link">
    <a href="{text()}">
      <xsl:value-of select="text()"/>
    </a>
    <xsl:text> </xsl:text>
  </xsl:template>
</xsl:stylesheet>
