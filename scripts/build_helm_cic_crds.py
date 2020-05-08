'''This script will generate cic_crds.yaml with helm conditions embedded in it. This script can be used to pull latest definitions of CRDs exposed to public and then generate cic_crds.yaml.
'''
import os

try:
    os.system("git clone https://github.com/citrix/citrix-k8s-ingress-controller/ /tmp/citrix-k8s-ingress-controller/")
    install_condition_start = "{{- if .Values.crds.install }}\n"
    install_condition_end = "{{- end }}"
    retainondelete_condition = \
'''{{- if .Values.crds.retainOnDelete }}
  annotations:
    "helm.sh/resource-policy": keep
{{- end }}\n'''

    crd_dir = '/tmp/citrix-k8s-ingress-controller/crd'
    crd_list = ["rewrite-responder-policies-deployment.yaml", "ratelimit/ratelimit-crd.yaml", "vip/vip.yaml", "auth/auth-crd.yaml", "contentrouting/Listener.yaml", "contentrouting/HTTPRoute.yaml", "canary/canary-crd-class.yaml"]

    out = open("cic_crds.yaml", 'w')
    out.write(install_condition_start)

    for crd_path in crd_list:
        with open(os.path.join(crd_dir, crd_path)) as crd_file:
            crd = crd_file.readlines()
            for line_num, line in enumerate(crd):
                if line.strip().startswith('name:'):
                    crd.insert(int(line_num)+1, retainondelete_condition)
                    break
            out.writelines(crd)
        out.write("---\n")

    out.write(install_condition_end)
    out.close()
    os.system("rm -rf /tmp/citrix-k8s-ingress-controller")
except Exception as e:
    print("Failed with exception " +  e)
    raise e
