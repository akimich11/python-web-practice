def calculate(data, findall):
	matches = findall(r"([abc])([+-]?=)([abc]?)([+-]?\d*)")
	for v1, s, v2, n in matches:
		if len(s) == 1:
			data[v1] = data.get(v2, 0) + int(n or 0)
		elif s[0] == '+':
			data[v1] += data.get(v2, 0) + int(n or 0)
		else:
			data[v1] -= data.get(v2, 0) + int(n or 0)

	return data
