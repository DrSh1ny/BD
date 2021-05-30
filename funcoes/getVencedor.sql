create or replace function getVencedor(
	p_id bigint
)returns infolicitacao
language 'plpgsql'
as $$
declare
    f record;
	f1 record;
	f2 record;
	lici infoLicitacao;
    c1 cursor(leilaoID bigint) for
        select *
		from licitacao
		where licitacao.leilao_id=leilaoID and licitacao.preco=(select max(preco) from licitacao where licitacao.leilao_id=leilaoID);
	c2 cursor(leilaoID bigint) for
        select *
		from leilao
		where leilao.id=leilaoID;
	c3 cursor(pessoaID bigint) for
        select *
		from pessoa
		where pessoa.id=pessoaID;
begin
	--check if auction exists
    open c2(p_id);
    fetch c2 into  f2;
	close c2;
	if(f2.data_fim>CURRENT_TIMESTAMP or not found) then
		lici.nome:='null';
		lici.preco:=-2;
		lici.data:=CURRENT_TIMESTAMP;
		return lici;
	end if;
	
	--check if auction has licitrations
	open c1(p_id);
	fetch c1 into f1;
	close c1;
	if(not found) then
		lici.nome:='null';
		lici.preco:=-1;
		lici.data:=CURRENT_TIMESTAMP;
		return lici;
	end if;
	
	--get person of last licitation
	open c3(f1.pessoa_id);
	fetch c3 into f;
	close c3;
	lici.nome:=f.nome;
	lici.preco:=f1.preco;
	lici.data:=f1.data;
	return lici;
end;
$$