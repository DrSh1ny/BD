create type infolicitacao as ( 
	nome varchar,
	preco bigint,
	data timestamp
);
   
CREATE OR REPLACE FUNCTION endAuction(
	p_id                  bigint
) returns infoLicitacao
LANGUAGE 'plpgsql'
AS $BODY$
declare
	f record;
	f1 record;
	f2 record;
	lici infoLicitacao;
	msg varchar;
	dt timestamp;
	novoID bigint;
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
	open c2(p_id);
	fetch c2 into f1;
	close c2;
	if(f1.data_fim>CURRENT_TIMESTAMP or not found) then
		lici.nome:='null';
		lici.preco:=-2;
		lici.data:=CURRENT_TIMESTAMP;
		return lici;
	end if;
	
    open c1(p_id);
	fetch c1 into f;
	close c1;
	if(not found) then
		lici.nome:='null';
		lici.preco:=-1;
		lici.data:=CURRENT_TIMESTAMP;
		msg:='O leilao ' || f1.id || ' terminou sem licitacoes';
		dt:=CURRENT_TIMESTAMP;
		insert into notificacao(mensagem,data) values(msg,dt) returning id into novoID;
		insert into notificacao_pessoa(lida,notificacao_id,pessoa_id) values(false,novoID,f1.pessoa_id);
		return lici;
	end if;
	open c3(f.pessoa_id);
	fetch c3 into f2;
	close c3;
	lici.nome:=f2.nome;
	lici.preco:=f.preco;
	lici.data:=f.data;
	msg:='O leilao ' || f.leilao_id || ' terminou com maxima licitacao de ' || f.preco || '€';
	dt:=CURRENT_TIMESTAMP;
	insert into notificacao(mensagem,data) values(msg,dt) returning id into novoID;
	insert into notificacao_pessoa(lida,notificacao_id,pessoa_id) values(false,novoID,f1.pessoa_id);
	return lici;
end;
$BODY$;