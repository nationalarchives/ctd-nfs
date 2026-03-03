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


	<!-- ignore 'doctype' text (should be 'AP') -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'doctype']"> </xsl:template>


	<!-- Display lastname, firstname -->
	<xsl:template mode="AncientPetitions" match="persname">
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
	</xsl:template>


	<!-- add petitioners -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'petitioners']">
		<tr class="medalRow">
			<td class="medalheader"> Petitioners: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>



	<!-- add Places mentioned -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'placesmentioned']">
		<tr class="medalRow">
			<td class="medalheader"> Places mentioned: </td>
			<td class="medalplain">
				<xsl:for-each select="./geogname">
					<xsl:value-of disable-output-escaping="yes" select="text()"/>
					<xsl:if test="following-sibling::geogname">
						<xsl:text disable-output-escaping="yes">; </xsl:text>
					</xsl:if>
				</xsl:for-each>
			</td>
		</tr>
	</xsl:template>


	<!-- add addressees -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'addressees']">
		<tr class="medalRow">
			<td class="medalheader"> Addressees: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>


	<!-- add occupation -->
	<xsl:template mode="AncientPetitions" match="occupation">
		<tr class="medalRow">
			<td class="medalheader"> Occupation: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>


	<!-- add date -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'date']">
		<tr class="medalRow">
			<td class="medalheader"> Date derivation: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>



	<!-- add request -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'request']">
		<tr class="medalRow">
			<td class="medalheader"> Nature of request: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>

	<!-- add endorsement -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'endorsement']">
		<tr class="medalRow">
			<td class="medalheader"> Nature of endorsement: </td>
			<td class="medalplain">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>


	<!-- add People mentioned -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'people']">
		<tr class="medalRow">
			<td class="medalheader"> People mentioned: </td>
			<td class="medalplain">
				<xsl:for-each select="./persname">
					<xsl:value-of disable-output-escaping="yes" select="text()"/>
					<xsl:if test="following-sibling::persname">
						<xsl:text disable-output-escaping="yes">; </xsl:text>
					</xsl:if>
				</xsl:for-each>
			</td>
		</tr>
	</xsl:template>


</xsl:stylesheet>
