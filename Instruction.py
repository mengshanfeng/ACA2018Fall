# Instruction.py
import Mem
import Reg
import pdb


def bindigits(n, bits):  # 实现十进制数字转成指定长度二进制字符串，用于存储
    s = bin(n & int("1" * bits, 2))[2:]
    return ("{0:0>%s}" % bits).format(s)


def LUI(rd, imm):  # LUI创建32位无符号整数，存放立即数到rd的高20位，低12位置0
    Reg.Register[rd] = bindigits(imm, 20) + bindigits(0, 12)
    Reg.PC += 1
    return


def AUIPC(rd, imm):  # AUIPC创建pc的相对地址，pc+无符号立即数(偏移量)=>rd
    Reg.Register[rd] = bindigits(Reg.PC + imm, 32)
    Reg.PC += 1
    return


def JAL(rd, imm):  # 立即数+pc为跳转目标，rd存放pc+4（返回地址）,跳转范围为pc(+/-)1MB
    Reg.Register[rd] = bindigits(Reg.PC + 1, 32)
    Reg.PC = Reg.PC + imm
    return


def JALR(rd, rs, imm):  # rs+立即数为跳转目标，rd存放pc+4（返回地址）,实现远跳转
    Reg.Register[rd] = bindigits(Reg.PC + 1, 32)
    Reg.PC = int(Reg.Register[rs], 2) + imm
    return


def BEQ(rs1, rs2, imm):  # rs1==rs2, 在相等时，发生跳转
    if rs1 == rs2:
        Reg.PC += imm
    else:
        Reg.PC += 1
    return


def BNE(rs1, rs2, imm):  # rs1!=rs2, 在不等时，发生跳转
    if rs1 != rs2:
        Reg.PC += imm
    else:
        Reg.PC += 1
    return


def BLT(rs1, rs2, imm):  # rs1 < rs2, 跳转
    if rs1 < rs2:
        Reg.PC += imm
    else:
        Reg.PC += 1
    return


def BGE(rs1, rs2, imm):  # rs1 >= rs2, 跳转
    if rs1 >= rs2:
        Reg.PC += imm
    else:
        Reg.PC += 1
    return


def BLTU(rs1, rs2, imm):  # 无符号，rs1 < rs2, 跳转
    if rs1 < rs2:
        Reg.PC += imm
    else:
        Reg.PC += 1
    return


def BGEU(rs1, rs2, imm):  # 无符号，rs1 >= rs2, 跳转
    if rs1 >= rs2:
        Reg.PC += imm
    else:
        Reg.PC += 1
    return


def LB(rd, rs, imm):  # 从存储器中读取一个字节的数据到寄存器中
    temp = bindigits(int(Mem.Memory[int(Reg.Register[rs], 2) + imm]), 32)[-8:]
    if int(temp[0]) == 0:
        Reg.Register[rd] = "000000000000000000000000" + temp
    else:
        Reg.Register[rd] = "111111111111111111111111" + temp
    Reg.PC += 1
    return


def LH(rd, rs, imm):  # 从存储器中读取半个字的数据到寄存器中
    temp = bindigits(int(Mem.Memory[int(Reg.Register[rs], 2) + imm]), 32)[-16:]
    if int(temp[0]) == 0:
        Reg.Register[rd] = "0000000000000000" + temp
    else:
        Reg.Register[rd] = "1111111111111111" + temp
    Reg.PC += 1
    return


def LW(rd, rs, imm):  # 从存储器中读取一个字的数据到寄存器中
    Reg.Register[rd] = bindigits(Mem.Memory[int(Reg.Register[rs], 2) + imm], 32)
    Reg.PC += 1
    return


def LBU(rd, rs, imm):  # 功能与LB指令相同，但读出的是不带符号的数据
    temp = bindigits(int(Mem.Memory[int(Reg.Register[rs], 2) + imm]), 32)[-8:]
    Reg.Register[rd] = "000000000000000000000000" + temp
    Reg.PC += 1
    return


def LHU(rd, rs, imm):  # 功能与LH指令相同，但读出的是不带符号的数据
    temp = bindigits(int(Mem.Memory[int(Reg.Register[rs], 2) + imm]), 32)[-16:]
    Reg.Register[rd] = "0000000000000000" + temp
    Reg.PC += 1
    return


def SB(rs1, rs2, imm):  # 把一个字节的数据从寄存器存储到存储器中
    Mem.Memory[int(Reg.Register[rs1], 2) + imm] = int(Reg.Register[rs2][-8:], 2)
    Reg.PC += 1
    return


def SH(rs1, rs2, imm):  # 把半个字的数据从寄存器存储到存储器中
    Mem.Memory[int(Reg.Register[rs1], 2) + imm] = int(Reg.Register[rs2][-16:], 2)
    Reg.PC += 1
    return


def SW(rs1, rs2, imm):  # 把一个字的数据从寄存器存储到存储器中
    Mem.Memory[int(Reg.Register[rs1], 2) + imm] = int(Reg.Register[rs2], 2)
    Reg.PC += 1
    return


def ADDI(rd, rs, imm):  # 将12位有符号立即数和rs相加，溢出忽略，直接使用结果的最低32bit，并存入rd
    temp = bindigits(int(Reg.Register[rs], 2) + imm, 32)
    Reg.Register[rd] = temp
    Reg.PC += 1
    return


def SLTI(rd, rs, imm):  # 如果rs小于立即数(都是有符号整数),将rd置1,否则置0
    if int(Reg.Register[rs], 2) < imm:
        Reg.Register[rd] = "1".zfill(32)
    else:
        Reg.Register[rd] = "0".zfill(32)
    Reg.PC += 1
    return


def SLTIU(rd, rs, imm):  # 和SLTI一致，不过都是无符号数
    if int(Reg.Register[rs], 2) < imm:
        Reg.Register[rd] = "1".zfill(32)
    else:
        Reg.Register[rd] = "0".zfill(32)
    Reg.PC += 1
    return


def XORI(rd, rs, imm):  # rs与有符号12位立即数进行xor操作，并将结果写入rd
    Reg.Register[rd] = bindigits(int(Reg.Register[rs], 2) ^ imm, 32)
    Reg.PC += 1
    return


def ORI(rd, rs, imm):  # rs与有符号12位立即数进行or操作，并将结果写入rd
    Reg.Register[rd] = bindigits(int(Reg.Register[rs], 2) | imm, 32)
    Reg.PC += 1
    return


def ANDI(rd, rs, imm):  # rs与有符号12位立即数进行and操作，并将结果写入rd
    Reg.Register[rd] = bindigits(int(Reg.Register[rs], 2) & imm, 32)
    Reg.PC += 1
    return


def shift(rs, i, direct):  # 移一位操作，rs为原串，i为补入字符，dir为移位方向
    if direct == 1:  # 左移
        rs = rs[1:] + i
    else:  # 右移
        rs = i + rs[:-1]
    return rs


def SLLI(rs, imm):  # 逻辑左移，低位移入0
    i = 0
    while i < imm:
        Reg.Register[rs] = shift(Reg.Register[rs], "0", 1)
        i = i + 1
    Reg.PC += 1
    return


def SRLI(rs, imm):  # 逻辑右移，高位移入0
    i = 0
    while i < imm:
        Reg.Register[rs] = shift(Reg.Register[rs], "0", 0)
        i = i + 1
    Reg.PC += 1
    return


def SRAI(rs, imm):  # 算数右移，符号移入高位
    i = 0
    while i < imm:
        Reg.Register[rs] = shift(Reg.Register[rs], "".join(Reg.Register[rs][0]), 0)
        i = i + 1
    Reg.PC += 1
    return


def ADD(rd, rs1, rs2):  # rs1 + rs2 => rd
    Reg.Register[rd] = bindigits(int(Reg.Register[rs1], 2) + int(Reg.Register[rs2], 2), 32)
    Reg.PC += 1
    return


def SUB(rd, rs1, rs2):  # rs1 - rs2 => rd
    Reg.Register[rd] = bindigits(int(Reg.Register[rs1], 2) - int(Reg.Register[rs2], 2), 32)
    Reg.PC += 1
    return


def SLL(rs1, rs2):  # 逻辑左移，低位移入0，将r2的低5位作为立即数
    temp = int(Reg.Register[rs2][-5:], 2)
    i = 0
    while i < temp:
        Reg.Register[rs1] = shift(Reg.Register[rs1], "0", 1)
        i = i + 1
    Reg.PC += 1
    return


def SLT(rd, rs1, rs2):  # 如果rs1<rs2，rd写1; 否则rd为0
    if int(Reg.Register[rs1], 2) < int(Reg.Register[rs2], 2):
        Reg.Register[rd] = "1".zfill(32)
    else:
        Reg.Register[rd] = "0".zfill(32)
    Reg.PC += 1
    return


def SLTU(rd, rs1, rs2):  # 如果rs1<rs2，rd写1; 否则rd为0
    if int(Reg.Register[rs1], 2) < int(Reg.Register[rs2], 2):
        Reg.Register[rd] = "1".zfill(32)
    else:
        Reg.Register[rd] = "0".zfill(32)
    Reg.PC += 1
    return


def XOR(rd, rs1, rs2):  # rs1与rs2进行xor操作
    Reg.Register[rd] = bindigits(int(Reg.Register[rs1], 2) ^ int(Reg.Register[rs2], 2), 32)
    Reg.PC += 1
    return


def SRL(rs1, rs2):  # 逻辑右移，高位移入0，将r2的低5位作为立即数
    temp = int(Reg.Register[rs2][-5:], 2)
    i = 0
    while i < temp:
        Reg.Register[rs1] = shift(Reg.Register[rs1], "0", 0)
        i = i + 1
    Reg.PC += 1
    return


def SRA(rs1, rs2):  # 算数右移，符号移入高位，将r2的低5位作为立即数
    temp = int(Reg.Register[rs2][-5:], 2)
    i = 0
    while i < temp:
        Reg.Register[rs1] = shift(Reg.Register[rs1], "".join(Reg.Register[rs1][0]), 0)
        i = i + 1
    Reg.PC += 1
    return


def OR(rd, rs1, rs2):  # rs1与rs2进行or操作
    Reg.Register[rd] = bindigits(int(Reg.Register[rs1], 2) | int(Reg.Register[rs2], 2), 32)
    Reg.PC += 1
    return


def AND(rd, rs1, rs2):  # rs1与rs2进行and操作
    Reg.Register[rd] = bindigits(int(Reg.Register[rs1], 2) & int(Reg.Register[rs2], 2), 32)
    Reg.PC += 1
    return


def FENCE(pi, po, pr, pw):  # FENCE之前所有的存储器操作、I/O操作必须完成后，在FENCE之后的指令才能看到结果。
    si = pi
    so = po
    sr = pr
    sw = pw
    print(si, so, sr, sw)
    Reg.PC += 1
    return


def FENCE_I():  # 保证在一个RISC-V线程中，该指令之后的取指操作，可以看得到这条指令之前的任何数据store。
    Reg.PC += 1
    return


def ECALL():  # 环境调用
    ECALL()
    return


def EBREAK():  # 断点
    pdb.set_trace()
    Reg.PC += 1
    return


def CSRRW(rd, rs):  # 读取CSR的值存入rd寄存器，并将rs存入CSR，另外：如果rd为x0,将不会执行
    if int(Reg.Register[rd], 2) != 0:
        Reg.Register[rd] = bindigits(Reg.CSR, 32)
        Reg.CSR = int(Reg.Register[rs], 2)
    Reg.PC += 1
    return


def CSRRS(rd, rs):  # 读取CSR的值存入rd寄存器，并根据rs中高位对CSR置1，另外：如果rs为x0,将不会执行
    if int(Reg.Register[rd], 2) != 0:
        Reg.Register[rd] = bindigits(Reg.CSR, 32)
        Reg.CSR = int(Reg.Register[rs][0])
    Reg.PC += 1
    return


def CSRRC(rd, rs):  # 读取CSR的值存入rd寄存器，并根据rs中高位对CSR置0，另外：如果rs为x0,将不会执行
    if int(Reg.Register[rd], 2) != 0:
        Reg.Register[rd] = bindigits(Reg.CSR, 32)
        if int(Reg.Register[rs][0]) == 1:
            Reg.CSR = 0
        else:
            Reg.CSR = 1
    Reg.PC += 1
    return


def CSRRWI(rd, imm):  # 读取CSR的值存入rd寄存器，并将立即数存入CSR，另外：如果立即数为0,将不会执行
    if imm != 0:
        Reg.Register[rd] = bindigits(Reg.CSR, 32)
        Reg.CSR = imm
    Reg.PC += 1
    return


def CSRRSI(rd, imm):  # 读取CSR的值存入rd寄存器，并根据立即数中高位对CSR置1，另外：如果立即数为0,将不会执行
    if imm != 0:
        Reg.Register[rd] = bindigits(Reg.CSR, 32)
        temp = bindigits(imm, 5)
        Reg.CSR = int(temp[0])
    Reg.PC += 1
    return


def CSRRCI(rd, imm):  # 读取CSR的值存入rd寄存器，并根据立即数中高位对CSR置0，另外：如果立即数为0,将不会执行
    if imm != 0:
        Reg.Register[rd] = bindigits(Reg.CSR, 32)
        temp = bindigits(imm, 5)
        if int(temp[0]) == 0:
            Reg.CSR = 1
        else:
            Reg.CSR = 0
    Reg.PC += 1
    return
