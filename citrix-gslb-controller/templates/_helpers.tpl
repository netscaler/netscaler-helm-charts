{{/* vim: set filetype=mustache: */}}
{{/*
fetching sitedata and creating a dict of sites 
*/}}
{{- define "citrix-gslb-controller.sites" -}}
{{- $sitesWithEnv := dict "sites" (list) -}}
{{- range $site := .Values.sitedata -}}
{{- $var := .siteName | append $sitesWithEnv.sites | set $sitesWithEnv "sites" -}}
{{- end -}}
{{ join "," $sitesWithEnv.sites }}
{{- end -}}

{{/*
Create keyname for siteip. Prefixed with sitename and postfixed with "_ip"
*/}}
{{- define "citrix-gslb-controller.siteip" -}}
{{ printf "%s_%s" .siteName "ip"}}
{{- end -}}

{{/*
Create keyname for siteusername. Prefixed with sitename and postfixed with "_username"
*/}}
{{- define "citrix-gslb-controller.siteusername" -}}
{{ printf "%s_%s" .siteName "username"}}
{{- end -}}

{{/*
Create keyname for sitepassword. Prefixed with sitename and postfixed with "_password"
*/}}
{{- define "citrix-gslb-controller.sitepassword" -}}
{{ printf "%s_%s" .siteName "password"}}
{{- end -}}

{{/*
Create keyname for siteregion. Prefixed with sitename and postfixed with "_region"
*/}}
{{- define "citrix-gslb-controller.siteregion" -}}
{{ printf "%s_%s" .siteName "region"}}
{{- end -}}
