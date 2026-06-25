<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html" encoding="utf-8"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 23/03/2006
		Modified.
		###	VERSION: 1.2 	AUTHOR: MHILLYARD	DATE: 01/06/2006
		Modified 'Places mentioned' to display only once (with all <geogname>s alongside semi-colon delimited)
		Specified "utf-8" for output.
		-->
	</xsl:template>


	<!-- ignore 'doctype' text (should be 'FS') -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'doctype']"> </xsl:template>

	<!-- add Farm name -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'farmNumber']">
		<tr class="medalRow">
			<td class="medalheader"> Farm number: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Farm name -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'farmName']">
		<tr class="medalRow">
			<td class="medalheader"> Farm or holding: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Addressee(s) -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'addressee']">
		<tr class="medalRow">
			<td class="medalheader"> Addressee(s): </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	# TODO: refactor 
	<!-- Display lastname, firstname -->
	<!-- <xsl:template mode="AncientPetitions" match="persname">
		<tr class="medalRow">
			<td class="medalheader" width="15%">
				<xsl:text disable-output-escaping="yes">Name(s): </xsl:text>
			</td>
			<td class="medalplain" width="35%">
				<xsl:value-of disable-output-escaping="yes"
					select="emph[@altrender = 'surname']/text()"/>
				<xsl:if test="emph[@altrender = 'surname'] and emph[@altrender = 'forenames']">
					<xsl:text disable-output-escaping="yes">, </xsl:text>
				</xsl:if>
				<xsl:value-of disable-output-escaping="yes"
					select="emph[@altrender = 'forenames']/text()"/>
			</td>
		</tr>
	</xsl:template> -->

	<!-- add Farmer(s) or Occupier(s) mentioned -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'farmer']">
		<tr class="medalRow">
			<td class="medalheader"> Farmer(s) or Occupier(s): </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Landowner(s) -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'landowner']">
		<tr class="medalRow">
			<td class="medalheader"> Landowner(s): </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Acreeage -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'acreage']">
		<tr class="medalRow">
			<td class="medalheader"> Acreage: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Appears on Ordnance Survey sheet(s) -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'os_sheet_number']">
		<tr class="medalRow">
			<td class="medalheader"> Appears on Ordnance Survey sheet(s): </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Field information date -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'field_info_date']">
		<tr class="medalRow">
			<td class="medalheader"> Field information date: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Primary farm record date -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'primary_record_date']">
		<tr class="medalRow">
			<td class="medalheader"> Primary farm record date: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Record consists of -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'forms']">
		<tr class="medalRow">
			<td class="medalheader"> Record consists of: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Forms present on other Records -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'additional_farms']">
		<tr class="medalRow">
			<td class="medalheader"> Forms present on other Records: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

</xsl:stylesheet>
