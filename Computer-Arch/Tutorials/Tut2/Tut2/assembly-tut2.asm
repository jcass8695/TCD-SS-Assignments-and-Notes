option casemap:none
includelib legacy_stdio_definitions.lib
extrn printf:near
.data
g			dq 4
string		db "a = %I64d b = %I64d c = %I64d d = %I64d e = %I64d sum = %I64d"

.code
public		minX64
; Remember parameters!
; rcx = a, rdx = b, r8 = c

minX64:
	push	rbp
	mov		rbp, rsp
	mov		rax, rcx				; v = a
	cmp		rdx, rax				; b - v
	jge		minX64_0
	mov		rax, rdx				; v = b
minX64_0:
	cmp		r8, rax					; c - v
	jge		minX64_1
	mov		rax, r8					; v = c
minX64_1:
	mov		rsp, rbp
	pop		rbp
	ret		0						; return v

public		pX64

pX64:
	push	rbp
	mov		rbp, rsp
	mov		[rbp - 16], rcx			; preserve parameters in own shadow space
	mov		[rbp - 24], rdx
	mov		[rbp - 32], r8
	mov		[rbp - 40], r9
	mov		r8, rdx					; c = j
	mov		rdx, rcx				; b = i
	mov		rcx, [g]				; a = [g]
	call	minX64					; return min in rax
	mov		r8, [rbp - 40]			; keep same shadow space for second min call
	mov		rdx, [rbp - 32]
	mov		rcx, rax
	call	minX64
	mov		rsp, rbp
	pop		rbp
	ret		0

public		gcdX64

gcdX64:
	push	rbp
	mov		rbp, rsp

	mov		rax, rcx
	mov		r10, rdx

	test	rdx, rdx
	je		gcdX64_0
	cqo
	idiv	r10
	mov		rcx, r10
	call	gcdX64					; gcd(b, a % b), don't allocate shadow space
gcdX64_0:
	test	rax, rax
	jns		gcdX64_1
	neg		rax
gcdX64_1:
	mov		rsp, rbp
	pop		rbp
	ret		0

public		qX64

qX64:
	push	rbp
	mov		rbp, rsp

	mov		rbx, rcx
	add		rbx, rdx
	add		rbx, r8
	add		rbx, r9
	add		rbx, [rbp + 48]

	push	rbx						; push sum for printf
	push	[rbp + 48]				; push parameter e for printf
	push	r9						; push parameter d for printf

	mov		r9, r8
	mov		r8, rdx
	mov		rdx, rcx
	lea		rcx, string
	sub		rsp, 32					; allocate shadow space
	call	printf
	add		rsp, 40					; deallocate shadow space + 2 pushed params
	pop		rax						; pop sum from stack

	mov		rsp, rbp
	pop		rbp
	ret		0

public		qX64_no_shadow			; should cause undefined behaviour and crash if called

qX64_no_shadow:
	push	rbp
	mov		rbp, rsp

	mov		rbx, rcx
	add		rbx, rdx
	add		rbx, r8
	add		rbx, r9
	add		rbx, [rbp + 48]

	push	rbx						; push sum for printf
	push	[rbp + 48]				; push parameter e for printf
	push	r9						; push parameter d for printf

	mov		r9, r8
	mov		r8, rdx
	mov		rdx, rcx
	lea		rcx, string
	call	printf
	add		rsp, 16					; deallocate 2 pushed params
	pop		rax						; pop sum from stack

	mov		rsp, rbp
	pop		rbp
	ret		0
			end