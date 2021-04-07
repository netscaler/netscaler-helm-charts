{{- define "exporter_nsip" -}}
{{- $match := .Values.ingressGateway.netscalerUrl | toString | regexFind "//.*[:]*" -}}
{{- $match | trimAll ":" | trimAll "/" -}}
{{- end -}}
