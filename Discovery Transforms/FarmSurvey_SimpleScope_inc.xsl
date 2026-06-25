<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 23/03/2006
		Modified.
		-->
	</xsl:template>


	<!-- ignore 'doctype' text (should be 'FS') -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'doctype']"> </xsl:template>


	<!-- Display lastname, firstname 
	<xsl:template mode="FarmSurvey" match="persname">
		<tr class="medalRow">
			<td class="medalheader" width="20%" width="20%">
				<xsl:text disable-output-escaping="yes">Name(s): </xsl:text>
			</td>
			<td class="medalplain" width="50%" width="50%">
				<xsl:value-of disable-output-escaping="yes"
					select="emph[@altrender = 'surname']/text()"/>
				<xsl:if test="emph[@altrender = 'surname'] and emph[@altrender = 'forenames']">
					<xsl:text disable-output-escaping="yes">, </xsl:text>
				</xsl:if>
				<xsl:value-of disable-output-escaping="yes"
					select="emph[@altrender = 'forenames']/text()"/>
			</td>
		</tr>
	</xsl:template>
	-->

	<!-- add Farm name -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'farmNumber']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Farm number: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Farm name -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'farmName']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Farm or holding: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Addressee(s) -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'addressee']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Addressee(s): </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Farmer(s) or Occupier(s) mentioned -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'farmer']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Farmer(s) or Occupier(s): </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Landowner(s) -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'landowner']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Landowner(s): </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Acreeage -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'acreage']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Acreage: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Appears on Ordnance Survey sheet(s) -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'os_sheet_number']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Appears on Ordnance Survey sheet(s): </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Field information date -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'field_info_date']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Field information date: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Primary farm record date -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'primary_record_date']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Primary farm record date: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Record consists of -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'forms']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Record consists of: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add Forms present on other Records -->
	<xsl:template mode="FarmSurvey" match="emph[@altrender = 'additional_farms']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Forms present on other Records: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

</xsl:stylesheet>
