option casemap:none
.data 
g	dq 4
.code

public min64
; Remember parameters!
; rcx = a, rdx = b, r8 = c

min64:
	push	rbp
	mov		rbp, rsp
	mov		rax, rcx				; v = a
	cmp		rdx, rax				; v - b
	jge		min_64_0
	mov		rax, rdx				; v = b
min_64_0:
	cmp		rax, r8					; v - c
	jge		min_64_1
	mov		rax, r8					; v = c
min_64_1:
	mov		rsp, rbp
	pop		rbp
	ret		0						; return v

;p_64:
;	push	rbp
;	mov		rbp, rsp
;	sub		rsp, 32					; create 32 bytes of shadow space for min call
;	mov		[rbp - 16], rcx			; preserve parameters in own shadow space
;	mov		[rbp - 24], rdx
;	mov		[rbp - 32], r8
;	mov		[rbp - 40], r9
;	mov		r8, rdx					; c = j
;	mov		rdx, rcx				; b = i
;	mov		rcx, [g]				; a = [g]
;	call	min_64					; return min in rax
;	mov		r8, [rbp - 40]			; keep same shadow space for second min call
;	mov		rdx, [rbp - 32]
;	mov		rcx, rax
;	call	min_64
;	add		rsp, 32					; unwind shadow space
;	mov		rsp, rbp
;	pop		rbp
;	ret		0

end