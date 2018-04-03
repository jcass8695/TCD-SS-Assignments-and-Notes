.686                                ; create 32 bit code
.model flat, C                      ; 32 bit memory model
 option casemap:none                ; case sensitive

.data 
g	dd	4

.code

public min
public p
public gcd

min:
	push	ebp						; Save old frame pointers
	mov		ebp, esp				; Init new frame pointer at current stack pointer position
	sub		esp, 4					; Allocate space for 1 local variable
	push	ebx						; Save non-volatile registers on the stack
	mov		eax, [ebp + 8]			; eax = parameter1
	mov		[ebp - 4], eax			; Local variable v = eax
	mov		eax, [ebp + 12]			; eax = parameter2
	cmp		eax, [ebp - 4]			; Compare eax to v
	jge		min0					; Branch if eax >= v
	mov		[ebp - 4], eax			; v = eax
min0:
	mov		eax, [ebp + 16]			; eax = parameter3
	cmp		eax, [ebp - 4]			; Compare eax to v
	jge		min1					; Branch if eax >= v
	mov		[ebp - 4], eax			; v = eax
min1:
	mov		eax, [ebp - 4]			; eax = v (for passing return value)
	pop		ebx						; Restore non-volatile registers
	mov		esp, ebp				; Deallocate local variables
	pop		ebp						; Restore old frame pointer
	ret		0						; return v

p:
	push	ebp						; Function enter boiler plate
	mov		ebp, esp
	sub		esp, 4
	push	ebx
	push	[ebp + 12]				; Push parameters for min function call
	push	[ebp + 8]
	push	[g]						; Push global g
	call	min
	add		esp, 12					; Deallocate parameters
	mov		[ebp - 4], eax			; v = min return value
	push	[ebp + 20]				; Push parameters for next min call
	push	[ebp + 16]
	push	[ebp - 4]
	call	min
	add		esp, 12					; Function exit boiler plate
	pop		ebx
	mov		esp, ebp
	pop		ebp
	ret		0

gcd:
	push	ebp						; Function enter boiler plate
	mov		ebp, esp
	push	ebx
	mov		eax, [ebp + 12]			; eax = parameter2
	test	eax, eax				; Test if eax = 0
	jne		gcd0					; Branch if eax != 0
	mov		eax, [ebp + 8]			; Return parameter1
	pop		ebx						; Function exit boiler plate
	mov		esp, ebp
	pop		ebp
	ret		0
gcd0:
	mov		eax, [ebp + 8]			; eax = parameter1
	and		edx, 0					; clear edx
	mov		ebx, [ebp + 12]			; ebx = parameter2
	div		ebx						; eax = eax / ebx & edx = eax % ebx (i.e. edx = remainder of eax / ebx)
	push	edx						; Push edx and ebx as parameters for recursive gcd call
	push	ebx
	call	gcd
	add		esp, 8					; Function exit boiler plate
	pop		ebx
	mov		esp, ebp
	pop		ebp
	ret		0

end