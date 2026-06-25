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


	<!-- ignore 'doctype' text (should be 'AP') -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'doctype']"> </xsl:template>


	<!-- Display lastname, firstname -->
	<xsl:template mode="AncientPetitions" match="persname">
		<tr class="medalRow">
			<td class="medalheader" width="20%">
				<xsl:text disable-output-escaping="yes">Name(s): </xsl:text>
			</td>
			<td class="medalplain" width="50%">
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


	<!-- add Petitioners -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'petitioners']">
		<xsl:variable name="petitioners" select="."/>
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Petitioners: </td>
			<td class="medalplain" width="50%">
				<!-- Truncate at the first available space between characters 120 and 130, otherwise at character 130 regardless -->
				<xsl:choose>
					<xsl:when test="substring($petitioners, 120, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 120)"/>
						<xsl:if test="string-length($petitioners) &gt; 120">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 121, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 121)"/>
						<xsl:if test="string-length($petitioners) &gt; 121">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 122, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 122)"/>
						<xsl:if test="string-length($petitioners) &gt; 122">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 123, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 123)"/>
						<xsl:if test="string-length($petitioners) &gt; 123">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 124, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 124)"/>
						<xsl:if test="string-length($petitioners) &gt; 124">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 125, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 125)"/>
						<xsl:if test="string-length($petitioners) &gt; 125">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 126, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 126)"/>
						<xsl:if test="string-length($petitioners) &gt; 126">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 127, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 127)"/>
						<xsl:if test="string-length($petitioners) &gt; 127">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 128, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 128)"/>
						<xsl:if test="string-length($petitioners) &gt; 128">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($petitioners, 129, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 129)"/>
						<xsl:if test="string-length($petitioners) &gt; 129">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of disable-output-escaping="yes"
							select="substring($petitioners, 1, 130)"/>
						<xsl:if test="string-length($petitioners) &gt; 130">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>



	<!-- add Addressees -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'addressees']">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Addressees: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>


	<!-- add places mentioned: -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'placesmentioned']">
		<xsl:variable name="placesmentioned">
			<xsl:for-each select="./geogname">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
				<xsl:if test="following-sibling::geogname">
					<xsl:text disable-output-escaping="yes">; </xsl:text>
				</xsl:if>
			</xsl:for-each>
		</xsl:variable>

		<tr class="medalRow">
			<td class="medalheader" width="20%"> Places mentioned: </td>
			<td class="medalplain" width="50%">
				<!-- Truncate at the first available space between characters 120 and 130, otherwise at character 130 regardless -->
				<xsl:choose>
					<xsl:when test="substring($placesmentioned, 120, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 120)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 120">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 121, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 121)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 121">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 122, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 122)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 122">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 123, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 123)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 123">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 124, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 124)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 124">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 125, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 125)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 125">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 126, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 126)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 126">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 127, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 127)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 127">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 128, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 128)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 128">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($placesmentioned, 129, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 129)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 129">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of disable-output-escaping="yes"
							select="substring($placesmentioned, 1, 130)"/>
						<xsl:if test="string-length($placesmentioned) &gt; 130">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>


	<!-- add people mentioned: -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'people']">
		<xsl:variable name="people">
			<xsl:for-each select="./persname">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
				<xsl:if test="following-sibling::persname">
					<xsl:text disable-output-escaping="yes">; </xsl:text>
				</xsl:if>
			</xsl:for-each>
		</xsl:variable>

		<tr class="medalRow">
			<td class="medalheader" width="20%"> People mentioned: </td>
			<td class="medalplain" width="50%">
				<!-- Truncate at the first available space between characters 120 and 130, otherwise at character 130 regardless -->
				<xsl:choose>
					<xsl:when test="substring($people, 120, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 120)"/>
						<xsl:if test="string-length($people) &gt; 120">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 121, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 121)"/>
						<xsl:if test="string-length($people) &gt; 121">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 122, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 122)"/>
						<xsl:if test="string-length($people) &gt; 122">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 123, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 123)"/>
						<xsl:if test="string-length($people) &gt; 123">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 124, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 124)"/>
						<xsl:if test="string-length($people) &gt; 124">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 125, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 125)"/>
						<xsl:if test="string-length($people) &gt; 125">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 126, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 126)"/>
						<xsl:if test="string-length($people) &gt; 126">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 127, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 127)"/>
						<xsl:if test="string-length($people) &gt; 127">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 128, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 128)"/>
						<xsl:if test="string-length($people) &gt; 128">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($people, 129, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 129)"/>
						<xsl:if test="string-length($people) &gt; 129">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of disable-output-escaping="yes"
							select="substring($people, 1, 130)"/>
						<xsl:if test="string-length($people) &gt; 130">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>


	<!-- add occupation -->
	<xsl:template mode="AncientPetitions" match="occupation">
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Occupation: </td>
			<td class="medalplain" width="50%">
				<xsl:value-of disable-output-escaping="yes" select="text()"/>
			</td>
		</tr>
	</xsl:template>


	<!-- add Date derivation: -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'date']">
		<xsl:variable name="date" select="."/>
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Date derivation: </td>
			<td class="medalplain" width="50%">
				<!-- Truncate at the first available space between characters 110 and 120, otherwise at character 120 regardless -->
				<xsl:choose>
					<xsl:when test="substring($date, 110, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 110)"/>
						<xsl:if test="string-length($date) &gt; 110">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 111, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 111)"/>
						<xsl:if test="string-length($date) &gt; 111">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 112, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 112)"/>
						<xsl:if test="string-length($date) &gt; 112">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 113, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 113)"/>
						<xsl:if test="string-length($date) &gt; 113">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 114, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 114)"/>
						<xsl:if test="string-length($date) &gt; 114">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 115, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 115)"/>
						<xsl:if test="string-length($date) &gt; 115">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 116, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 116)"/>
						<xsl:if test="string-length($date) &gt; 116">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 117, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 117)"/>
						<xsl:if test="string-length($date) &gt; 117">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 118, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 118)"/>
						<xsl:if test="string-length($date) &gt; 118">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($date, 119, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 119)"/>
						<xsl:if test="string-length($date) &gt; 119">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of disable-output-escaping="yes"
							select="substring($date, 1, 120)"/>
						<xsl:if test="string-length($date) &gt; 120">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>

	<!-- add Nature of Request: -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'request']">
		<xsl:variable name="request" select="."/>
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Nature of Request: </td>
			<td class="medalplain" width="50%">
				<!-- Truncate at the first available space between characters 120 and 130, otherwise at character 130 regardless -->
				<xsl:choose>
					<xsl:when test="substring($request, 120, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 120)"/>
						<xsl:if test="string-length($request) &gt; 120">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 121, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 121)"/>
						<xsl:if test="string-length($request) &gt; 121">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 122, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 122)"/>
						<xsl:if test="string-length($request) &gt; 122">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 123, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 123)"/>
						<xsl:if test="string-length($request) &gt; 123">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 124, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 124)"/>
						<xsl:if test="string-length($request) &gt; 124">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 125, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 125)"/>
						<xsl:if test="string-length($request) &gt; 125">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 126, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 126)"/>
						<xsl:if test="string-length($request) &gt; 126">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 127, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 127)"/>
						<xsl:if test="string-length($request) &gt; 127">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 128, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 128)"/>
						<xsl:if test="string-length($request) &gt; 128">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($request, 129, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 129)"/>
						<xsl:if test="string-length($request) &gt; 129">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of disable-output-escaping="yes"
							select="substring($request, 1, 130)"/>
						<xsl:if test="string-length($request) &gt; 130">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>


	<!-- add Nature of Endorsement: -->
	<xsl:template mode="AncientPetitions" match="emph[@altrender = 'endorsement']">
		<xsl:variable name="endorsement" select="."/>
		<tr class="medalRow">
			<td class="medalheader" width="20%"> Nature of Endorsement: </td>
			<td class="medalplain" width="50%">
				<!-- Truncate at the first available space between characters 120 and 130, otherwise at character 130 regardless -->
				<xsl:choose>
					<xsl:when test="substring($endorsement, 120, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 120)"/>
						<xsl:if test="string-length($endorsement) &gt; 120">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 121, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 121)"/>
						<xsl:if test="string-length($endorsement) &gt; 121">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 122, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 122)"/>
						<xsl:if test="string-length($endorsement) &gt; 122">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 123, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 123)"/>
						<xsl:if test="string-length($endorsement) &gt; 123">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 124, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 124)"/>
						<xsl:if test="string-length($endorsement) &gt; 124">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 125, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 125)"/>
						<xsl:if test="string-length($endorsement) &gt; 125">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 126, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 126)"/>
						<xsl:if test="string-length($endorsement) &gt; 126">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 127, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 127)"/>
						<xsl:if test="string-length($endorsement) &gt; 127">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 128, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 128)"/>
						<xsl:if test="string-length($endorsement) &gt; 128">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:when test="substring($endorsement, 129, 1) = ' '">
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 129)"/>
						<xsl:if test="string-length($endorsement) &gt; 129">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of disable-output-escaping="yes"
							select="substring($endorsement, 1, 130)"/>
						<xsl:if test="string-length($endorsement) &gt; 130">
							<xsl:text>...</xsl:text>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>


</xsl:stylesheet>
