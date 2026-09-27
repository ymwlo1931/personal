---
title: "default"
date: 1970-01-01
draft: false
---

+++
date = '{{ .Date }}'
draft = true
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
+++
